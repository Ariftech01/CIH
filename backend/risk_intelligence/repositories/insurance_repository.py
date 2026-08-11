from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.insurance_assessment import InsuranceAssessment

class InsuranceAssessmentRepository(BaseRepository[InsuranceAssessment]):
    def __init__(self, session: Session):
        super().__init__(InsuranceAssessment, session)

    def get_by_project(self, project_id: str) -> List[InsuranceAssessment]:
        stmt = (
            select(InsuranceAssessment)
            .where(InsuranceAssessment.project_id == project_id)
            .where(InsuranceAssessment.is_deleted == False)
            .order_by(desc(InsuranceAssessment.evaluated_at))
        )
        return list(self.session.execute(stmt).scalars().all())
