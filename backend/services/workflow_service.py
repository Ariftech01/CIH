from typing import List, Optional
from backend.database.session import get_db_session
from backend.repositories.workflow_repository import WorkflowRepository
from backend.schemas.workflow import WorkflowStateResponse, WorkflowHistoryResponse
from backend.workflow.workflow_engine import workflow_engine

class WorkflowService:
    def get_workflow_state(self, project_id: str) -> WorkflowStateResponse:
        with get_db_session() as session:
            repo = WorkflowRepository(session)
            ws = repo.get_or_create(project_id)
            return WorkflowStateResponse.model_validate(ws)

    def transition_stage(self, project_id: str, to_stage: str, action: str, performed_by: str = None) -> WorkflowStateResponse:
        return workflow_engine.transition_stage(project_id, to_stage, action, performed_by)

    def get_history(self, project_id: str) -> List[WorkflowHistoryResponse]:
        with get_db_session() as session:
            repo = WorkflowRepository(session)
            history = repo.get_project_history(project_id)
            return [WorkflowHistoryResponse.model_validate(h) for h in history]

workflow_service = WorkflowService()
