from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.risk_recommendation import RiskRecommendation

class RecommendationRepository(BaseRepository[RiskRecommendation]):
    def __init__(self, session: Session):
        super().__init__(RiskRecommendation, session)

    def get_active_by_project(self, project_id: str) -> List[RiskRecommendation]:
        stmt = (
            select(RiskRecommendation)
            .where(RiskRecommendation.project_id == project_id)
            .where(RiskRecommendation.resolution_status == "OPEN")
            .where(RiskRecommendation.is_deleted == False)
            .order_by(desc(RiskRecommendation.created_at))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_priority(self, project_id: str, priority: str) -> List[RiskRecommendation]:
        stmt = (
            select(RiskRecommendation)
            .where(RiskRecommendation.project_id == project_id)
            .where(RiskRecommendation.priority == priority)
            .where(RiskRecommendation.is_deleted == False)
            .order_by(desc(RiskRecommendation.created_at))
        )
        return list(self.session.execute(stmt).scalars().all())
