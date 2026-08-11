from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.risk_snapshot import RiskSnapshot

class RiskSnapshotRepository(BaseRepository[RiskSnapshot]):
    def __init__(self, session: Session):
        super().__init__(RiskSnapshot, session)

    def get_latest_snapshot(self, project_id: str) -> Optional[RiskSnapshot]:
        stmt = (
            select(RiskSnapshot)
            .where(RiskSnapshot.project_id == project_id)
            .where(RiskSnapshot.is_deleted == False)
            .order_by(desc(RiskSnapshot.captured_at))
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()
