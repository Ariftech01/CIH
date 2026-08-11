from typing import Dict, Any
from backend.database.session import get_db_session
from backend.repositories.task_repository import TaskRepository
from backend.repositories.notification_repository import NotificationRepository
from backend.workflow.workflow_engine import workflow_engine
from backend.risk_intelligence.automation.notification_engine import notification_engine
from backend.app_logging.logger import logger

class AutomationEngine:
    """
    Event-driven Automation Engine auto-generating default project tasks and processing workflow event hooks.
    Integrated with CRIE Risk Intelligence events, Notification Engine, and Background Services.
    """

    def handle_event(self, event_name: str, payload: Dict[str, Any]):
        logger.info(f"Automation Engine Event Triggered: '{event_name}' for payload {payload}")
        project_id = payload.get("project_id")

        if event_name == "ProjectCreated" and project_id:
            self._generate_default_tasks(project_id)
            self._notify(project_id, "Project Created", f"Project '{payload.get('project_name', 'New Project')}' initialized with default tasks.")
            workflow_engine.transition_stage(project_id, "PLANNING", "Tasks Auto-Generated")
            notification_engine.dispatch_notification("PROJECT_CREATED", "New Project Initialized", f"Project '{payload.get('project_name')}' created.", priority="INFORMATIONAL")

        elif event_name == "BuildingSaved" and project_id:
            workflow_engine.update_flag(project_id, "building_designed", True)
            workflow_engine.transition_stage(project_id, "DESIGN", "Building Designed")
            self._notify(project_id, "Building Saved", "3D Building model persisted and quantified successfully.")
            notification_engine.dispatch_notification("BUILDING_SAVED", "3D Model Saved", "Building geometry & BOM persisted.", priority="LOW")

        elif event_name == "CostEstimated" and project_id:
            workflow_engine.update_flag(project_id, "cost_estimated", True)
            workflow_engine.transition_stage(project_id, "ESTIMATION", "Cost Estimated")
            self._notify(project_id, "Cost Estimate Generated", f"Total estimated cost: {payload.get('estimated_total_cost', 0)}")
            notification_engine.dispatch_notification("COST_ESTIMATED", "Budget Estimated", f"Cost estimate generated: ${payload.get('estimated_total_cost', 0):,.2f}", priority="MEDIUM")

        elif event_name == "SafetyCompleted" and project_id:
            workflow_engine.update_flag(project_id, "safety_inspected", True)
            workflow_engine.transition_stage(project_id, "EXECUTION", "Safety Passed")
            notification_engine.dispatch_notification("SAFETY_COMPLETED", "Safety Audit Complete", "Workforce safety checklist & hazard evaluation completed.", priority="MEDIUM")

        elif event_name == "RiskAssessmentCompleted" and project_id:
            notification_engine.dispatch_notification("RISK_ASSESSMENT_COMPLETED", "CRIE Assessment Completed", f"Overall Risk Score: {payload.get('overall_risk_score', 0.0):.1f}/100 ({payload.get('risk_level', 'LOW')})", priority="HIGH")

        elif event_name == "ReportGenerated" and project_id:
            notification_engine.dispatch_notification("REPORT_GENERATED", "Enterprise Report Synthesized", f"Report '{payload.get('report_id')}' generated successfully.", priority="LOW")

    def _generate_default_tasks(self, project_id: str):
        default_tasks = [
            ("Project Planning & Design Review", "Planning", "HIGH"),
            ("Site Excavation & Foundation Preparation", "Foundation", "CRITICAL"),
            ("Structural Rebar & Concrete Framework", "Structure", "HIGH"),
            ("Electrical Conduit & Wiring Installation", "Electrical", "MEDIUM"),
            ("Plumbing & Drainage Pipe Fitting", "Plumbing", "MEDIUM"),
            ("Interior Plaster & Wall Finishing", "Finishing", "MEDIUM"),
            ("Final Safety & Quality Inspection", "Inspection", "HIGH"),
        ]
        with get_db_session() as session:
            t_repo = TaskRepository(session)
            for title, category, priority in default_tasks:
                t_repo.create({
                    "project_id": project_id,
                    "task_name": title,
                    "task_category": category,
                    "priority": priority,
                    "status": "PENDING"
                })

    def _notify(self, project_id: str, title: str, message: str, notification_type: str = "INFO"):
        with get_db_session() as session:
            n_repo = NotificationRepository(session)
            n_repo.create({
                "project_id": project_id,
                "title": title,
                "message": message,
                "notification_type": notification_type
            })

automation_engine = AutomationEngine()
