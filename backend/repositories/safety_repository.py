from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.safety import SafetyInspection
from backend.repositories.base_repository import BaseRepository

class SafetyRepository(BaseRepository[SafetyInspection]):
    def __init__(self, session: Session):
        super().__init__(SafetyInspection, session)

    def get_by_project(self, project_id: str) -> List[SafetyInspection]:
        stmt = select(SafetyInspection).where(SafetyInspection.project_id == project_id, SafetyInspection.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_open_inspections(self, project_id: str = None) -> List[SafetyInspection]:
        stmt = select(SafetyInspection).where(SafetyInspection.status == "OPEN", SafetyInspection.is_deleted == False)
        if project_id:
            stmt = stmt.where(SafetyInspection.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())

    def get_high_risk_inspections(self, project_id: str = None) -> List[SafetyInspection]:
        stmt = select(SafetyInspection).where(
            SafetyInspection.risk_level.in_(["HIGH", "CRITICAL"]),
            SafetyInspection.is_deleted == False
        )
        if project_id:
            stmt = stmt.where(SafetyInspection.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())
