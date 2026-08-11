from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.approval import Approval
from backend.repositories.base_repository import BaseRepository

class ApprovalRepository(BaseRepository[Approval]):
    def __init__(self, session: Session):
        super().__init__(Approval, session)

    def get_by_project(self, project_id: str) -> List[Approval]:
        stmt = select(Approval).where(Approval.project_id == project_id, Approval.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_pending(self, project_id: str = None) -> List[Approval]:
        stmt = select(Approval).where(Approval.status == "PENDING", Approval.is_deleted == False)
        if project_id:
            stmt = stmt.where(Approval.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())
