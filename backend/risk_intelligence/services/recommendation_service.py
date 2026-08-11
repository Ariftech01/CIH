from typing import List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.recommendation_repository import RecommendationRepository
from backend.risk_intelligence.models.risk_recommendation import RiskRecommendation

class RecommendationService:
    def get_active_recommendations(self, project_id: str) -> List[RiskRecommendation]:
        with get_db_session() as session:
            repo = RecommendationRepository(session)
            return repo.get_active_by_project(project_id)

    def mark_resolved(self, recommendation_id: str) -> bool:
        with get_db_session() as session:
            repo = RecommendationRepository(session)
            rec = repo.get_by_id(recommendation_id)
            if rec:
                rec.resolution_status = "RESOLVED"
                session.flush()
                return True
            return False

recommendation_service = RecommendationService()
