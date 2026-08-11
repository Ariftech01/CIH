from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.project_risk_score import ProjectRiskScore

class ProjectRiskScoreRepository(BaseRepository[ProjectRiskScore]):
    def __init__(self, session: Session):
        super().__init__(ProjectRiskScore, session)

    def get_by_assessment(self, assessment_id: str) -> List[ProjectRiskScore]:
        stmt = (
            select(ProjectRiskScore)
            .where(ProjectRiskScore.assessment_id == assessment_id)
            .where(ProjectRiskScore.is_deleted == False)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_latest_by_category(self, project_id: str, category: str) -> Optional[ProjectRiskScore]:
        stmt = (
            select(ProjectRiskScore)
            .where(ProjectRiskScore.project_id == project_id)
            .where(ProjectRiskScore.category == category)
            .where(ProjectRiskScore.is_deleted == False)
            .order_by(desc(ProjectRiskScore.calculated_at))
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()
