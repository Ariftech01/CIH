from typing import Dict, Any, List, Optional
from backend.database.session import get_db_session
from backend.repositories.project_repository import ProjectRepository
from backend.repositories.material_repository import MaterialRepository
from backend.repositories.worker_repository import WorkerRepository
from backend.repositories.equipment_repository import EquipmentRepository
from backend.repositories.safety_repository import SafetyRepository
from backend.repositories.report_repository import ReportRepository
from backend.cache.cache_manager import cache_manager
from backend.app_logging.logger import db_logger

class AnalyticsEngine:
    """
    Enterprise Analytics & KPI aggregation engine for Agentic AI for Safety Monitoring with Construction Risk Analytics.
    """
    def get_dashboard_kpis(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        cache_key = f"dashboard_kpis_{project_id}" if project_id else "dashboard_kpis"
        cached = cache_manager.get(cache_key)
        if cached:
            return cached

        try:
            with get_db_session() as session:
                proj_repo = ProjectRepository(session)
                mat_repo = MaterialRepository(session)
                wrk_repo = WorkerRepository(session)
                eq_repo = EquipmentRepository(session)
                sft_repo = SafetyRepository(session)
                rep_repo = ReportRepository(session)

                total_projects = proj_repo.count()
                active_projects = len(proj_repo.get_active_projects())
                completed_projects = len(proj_repo.get_completed_projects())
                
                total_materials = mat_repo.count()
                total_workers = wrk_repo.count()
                active_workers = len(wrk_repo.get_active_workers())
                
                total_equipment = eq_repo.count()
                operational_eq = len(eq_repo.get_operational_equipment())
                
                open_safety = len(sft_repo.get_open_inspections())
                high_risk_safety = len(sft_repo.get_high_risk_inspections())
                
                total_reports = rep_repo.count()

                result = {
                    "total_projects": total_projects,
                    "active_projects": active_projects,
                    "completed_projects": completed_projects,
                    "in_progress_projects": active_projects,
                    "total_materials": total_materials,
                    "total_workers": total_workers,
                    "active_workers": active_workers,
                    "total_equipment": total_equipment,
                    "operational_equipment": operational_eq,
                    "open_safety_inspections": open_safety,
                    "high_risk_inspections": high_risk_safety,
                    "total_reports": total_reports,
                }

                cache_manager.set(cache_key, result, ttl_seconds=60)
                return result
        except Exception as e:
            db_logger.error(f"Failed to fetch dashboard KPIs from database: {str(e)}")
            return {
                "total_projects": 0,
                "active_projects": 0,
                "completed_projects": 0,
                "in_progress_projects": 0,
                "total_materials": 0,
                "total_workers": 0,
                "active_workers": 0,
                "total_equipment": 0,
                "operational_equipment": 0,
                "open_safety_inspections": 0,
                "high_risk_inspections": 0,
                "total_reports": 0,
            }

analytics_engine = AnalyticsEngine()
