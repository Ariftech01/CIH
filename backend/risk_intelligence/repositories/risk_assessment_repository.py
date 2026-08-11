from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.risk_assessment import RiskAssessment

class RiskAssessmentRepository(BaseRepository[RiskAssessment]):
    def __init__(self, session: Session):
        super().__init__(RiskAssessment, session)

    def get_latest_by_project(self, project_id: str) -> Optional[RiskAssessment]:
        stmt = (
            select(RiskAssessment)
            .where(RiskAssessment.project_id == project_id)
            .where(RiskAssessment.is_deleted == False)
            .order_by(desc(RiskAssessment.evaluated_at))
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_project_history(self, project_id: str, limit: int = 50) -> List[RiskAssessment]:
        stmt = (
            select(RiskAssessment)
            .where(RiskAssessment.project_id == project_id)
            .where(RiskAssessment.is_deleted == False)
            .order_by(desc(RiskAssessment.evaluated_at))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())
