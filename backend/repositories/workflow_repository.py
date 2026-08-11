from typing import Optional, List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.models.workflow_state import WorkflowState, WorkflowHistory
from backend.repositories.base_repository import BaseRepository

class WorkflowRepository(BaseRepository[WorkflowState]):
    def __init__(self, session: Session):
        super().__init__(WorkflowState, session)
        self.history_repo = BaseRepository(WorkflowHistory, session)

    def get_by_project(self, project_id: str) -> Optional[WorkflowState]:
        stmt = select(WorkflowState).where(WorkflowState.project_id == project_id, WorkflowState.is_deleted == False)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_or_create(self, project_id: str) -> WorkflowState:
        ws = self.get_by_project(project_id)
        if not ws:
            ws = self.create({"project_id": project_id, "current_stage": "DRAFT", "current_status": "Project Created"})
        return ws

    def log_history(self, project_id: str, from_stage: str, to_stage: str, action: str, performed_by: str = None, notes: str = None) -> WorkflowHistory:
        return self.history_repo.create({
            "project_id": project_id,
            "from_stage": from_stage,
            "to_stage": to_stage,
            "action": action,
            "performed_by": performed_by,
            "notes": notes
        })

    def get_project_history(self, project_id: str) -> List[WorkflowHistory]:
        stmt = select(WorkflowHistory).where(WorkflowHistory.project_id == project_id).order_by(desc(WorkflowHistory.timestamp))
        return list(self.session.execute(stmt).scalars().all())
