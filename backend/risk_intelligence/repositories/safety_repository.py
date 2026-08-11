from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.safety_assessment import SafetyAssessment

class SafetyAssessmentRepository(BaseRepository[SafetyAssessment]):
    def __init__(self, session: Session):
        super().__init__(SafetyAssessment, session)

    def get_by_project(self, project_id: str, limit: int = 50) -> List[SafetyAssessment]:
        stmt = (
            select(SafetyAssessment)
            .where(SafetyAssessment.project_id == project_id)
            .where(SafetyAssessment.is_deleted == False)
            .order_by(desc(SafetyAssessment.assessed_at))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())
