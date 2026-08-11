from datetime import datetime
from typing import Optional, Dict, Any
from backend.database.session import get_db_session
from backend.repositories.workflow_repository import WorkflowRepository
from backend.repositories.project_repository import ProjectRepository
from backend.schemas.workflow import WorkflowStateResponse
from backend.cache.cache_manager import cache_manager
from backend.app_logging.logger import logger

class WorkflowEngine:
    """
    Central Orchestrator managing project lifecycle stages and workflow state transitions.
    Stages: DRAFT -> PLANNING -> DESIGN -> ESTIMATION -> EXECUTION -> MONITORING -> COMPLETED -> ARCHIVED
    """
    def initialize_project_workflow(self, project_id: str) -> WorkflowStateResponse:
        with get_db_session() as session:
            repo = WorkflowRepository(session)
            ws = repo.get_or_create(project_id)
            repo.log_history(project_id, "NONE", "DRAFT", "Project Initialized", notes="Workflow Engine auto-initialized.")
            return WorkflowStateResponse.model_validate(ws)

    def transition_stage(self, project_id: str, to_stage: str, action_name: str, performed_by: str = None, notes: str = None) -> WorkflowStateResponse:
        with get_db_session() as session:
            w_repo = WorkflowRepository(session)
            p_repo = ProjectRepository(session)
            
            ws = w_repo.get_or_create(project_id)
            from_stage = ws.current_stage
            
            ws.current_stage = to_stage
            ws.current_status = action_name
            ws.last_transition_at = datetime.utcnow()
            
            # Map workflow stage to project status
            proj = p_repo.get_by_id(project_id)
            if proj:
                if to_stage in ["DRAFT", "PLANNING"]:
                    proj.status = "PLANNED"
                elif to_stage in ["DESIGN", "ESTIMATION", "EXECUTION", "MONITORING"]:
                    proj.status = "IN_PROGRESS"
                elif to_stage == "COMPLETED":
                    proj.status = "COMPLETED"
                elif to_stage == "ARCHIVED":
                    proj.status = "CANCELLED"
            
            w_repo.log_history(project_id, from_stage, to_stage, action_name, performed_by, notes)
            cache_manager.invalidate("dashboard")
            logger.info(f"Workflow Transition for Project '{project_id}': {from_stage} -> {to_stage} ({action_name})")
            return WorkflowStateResponse.model_validate(ws)

    def update_flag(self, project_id: str, flag_name: str, value: bool = True) -> WorkflowStateResponse:
        with get_db_session() as session:
            w_repo = WorkflowRepository(session)
            ws = w_repo.get_or_create(project_id)
            if hasattr(ws, flag_name):
                setattr(ws, flag_name, value)
                ws.last_transition_at = datetime.utcnow()
            return WorkflowStateResponse.model_validate(ws)

workflow_engine = WorkflowEngine()
