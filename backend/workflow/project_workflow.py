"""Enterprise Project Workflow & Cross-Module Synchronization Coordinator."""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import streamlit as st

from backend.database.session import get_db_session
from backend.repositories.project_repository import ProjectRepository
from backend.services.project_service import project_service
from backend.schemas.project import ProjectResponse, ProjectUpdate
from backend.workflow.workflow_engine import workflow_engine
from backend.automation.automation_engine import automation_engine
from backend.cache.cache_manager import cache_manager
from backend.app_logging.logger import logger


class ProjectWorkflowCoordinator:
    """Centralized coordinator managing active project lifecycle, 3D auto-fill sync, and cross-module context."""

    def set_active_project(self, project_id_or_code: str) -> Optional[ProjectResponse]:
        """Set active enterprise project across all CIH modules."""
        if not project_id_or_code:
            return None

        # Look up by ID or Code
        proj = None
        try:
            proj = project_service.get_project_by_id(project_id_or_code)
        except Exception:
            pass

        if not proj:
            try:
                proj = project_service.get_project_by_code(project_id_or_code)
            except Exception:
                pass

        if proj:
            st.session_state["active_project_id"] = proj.id
            st.session_state["active_project_code"] = proj.project_code
            st.session_state["active_project_name"] = proj.project_name
            st.session_state["_active_project_obj"] = proj
            cache_manager.set("cih_active_project_id", proj.id, ttl_seconds=3600)
            cache_manager.set("cih_active_project_code", proj.project_code, ttl_seconds=3600)
            
            # Invalidate project-dependent function caches on project switch
            try:
                from modules.dashboard import _get_cached_dashboard_context
                _get_cached_dashboard_context.clear()
            except Exception:
                pass

            try:
                from modules.construction_risk import _get_cached_cri_context
                _get_cached_cri_context.clear()
            except Exception:
                pass

            try:
                from services.ollamaService import get_module_context
                get_module_context.clear()
            except Exception:
                pass

            try:
                cache_manager.invalidate("dashboard_kpis")
                cache_manager.invalidate(f"dashboard_kpis_{proj.id}")
            except Exception:
                pass

            logger.info(f"Active project switched to: '{proj.project_name}' ({proj.project_code})")
            return proj

        # Store fallback in session state
        st.session_state["active_project_id"] = project_id_or_code
        st.session_state["active_project_code"] = project_id_or_code
        st.session_state.pop("_active_project_obj", None)
        return None

    def get_active_project(self) -> Optional[ProjectResponse]:
        """Retrieve current active enterprise project (cached in session state)."""
        active_id = st.session_state.get("active_project_id") or cache_manager.get("cih_active_project_id")

        cached_obj = st.session_state.get("_active_project_obj")
        if cached_obj and getattr(cached_obj, "id", None) == active_id:
            return cached_obj

        if not active_id:
            # Fallback to first database project or None
            all_projs = project_service.get_all_projects(limit=1)
            if all_projs:
                active_id = all_projs[0].id
                return self.set_active_project(active_id)
            return None

        try:
            proj = project_service.get_project_by_id(active_id)
            if proj:
                return self.set_active_project(proj.id)
            return None
        except Exception:
            return None

    def sync_3d_metrics_to_project(
        self,
        project_id_or_code: str,
        scene_metrics: Dict[str, Any],
        geometry_json: str,
        version_note: Optional[str] = "3D Studio Update",
        create_new_version: bool = False
    ) -> ProjectResponse:
        """Automatically transfer 3D visualizer metrics into master project record and save version."""
        proj = self.set_active_project(project_id_or_code)
        if not proj:
            raise ValueError(f"Enterprise project '{project_id_or_code}' not found in registry.")

        project_id = proj.id

        with get_db_session() as session:
            repo = ProjectRepository(session)
            db_proj = repo.get_by_id(project_id)
            if not db_proj:
                raise ValueError(f"Project ID {project_id} not found in database.")

            # Auto-fill building metrics calculated from 3D geometry
            if "total_builtup_area" in scene_metrics:
                db_proj.total_builtup_area = float(scene_metrics["total_builtup_area"])
            if "number_of_floors" in scene_metrics:
                db_proj.number_of_floors = int(scene_metrics["number_of_floors"])
            if "number_of_rooms" in scene_metrics:
                db_proj.number_of_rooms = int(scene_metrics["number_of_rooms"])
            if "construction_area" in scene_metrics:
                db_proj.construction_area = float(scene_metrics["construction_area"])
            if "building_type" in scene_metrics:
                db_proj.building_type = str(scene_metrics["building_type"])

            # Store geometry JSON snapshot
            db_proj.model_geometry_json = geometry_json

            # Versioning Engine (V1.0 -> V1.1 / V2.0)
            history = []
            if db_proj.version_history_json:
                try:
                    history = json.loads(db_proj.version_history_json)
                except Exception:
                    history = []

            curr_ver_str = db_proj.current_version or "V1.0"
            if create_new_version:
                major_num = int(curr_ver_str.replace("V", "").split(".")[0]) + 1
                curr_ver_str = f"V{major_num}.0"
                db_proj.current_version = curr_ver_str

            version_entry = {
                "version": curr_ver_str,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "editor": st.session_state.get("user_id", "Senior BIM Engineer"),
                "note": version_note,
                "metrics": scene_metrics,
                "geometry_snapshot": geometry_json[:500] + "..." if geometry_json else ""
            }
            history.append(version_entry)
            db_proj.version_history_json = json.dumps(history)

            session.commit()
            session.refresh(db_proj)

            # Advance workflow transition if in planning stage
            workflow_engine.transition_stage(
                project_id=project_id,
                to_stage="DESIGN",
                action_name="3D Model Synchronized",
                notes=f"Synced 3D geometry version {curr_ver_str}"
            )

            # Broadcast automation event to invalidate caches
            automation_engine.handle_event("Project3DSynced", {
                "project_id": project_id,
                "project_name": db_proj.project_name,
                "version": curr_ver_str
            })

            cache_manager.invalidate("dashboard")
            return ProjectResponse.model_validate(db_proj)

    def get_project_version_history(self, project_id: str) -> List[Dict[str, Any]]:
        """Retrieve complete version history stack for enterprise project."""
        try:
            proj = project_service.get_project_by_id(project_id)
            if proj and proj.version_history_json:
                return json.loads(proj.version_history_json)
        except Exception:
            pass
        return []


project_workflow = ProjectWorkflowCoordinator()
