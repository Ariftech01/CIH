from typing import List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.trend_repository import TrendRepository
from backend.risk_intelligence.models.risk_trend import RiskTrend

class TrendService:
    def get_trends(self, project_id: str, period_type: str = "WEEKLY") -> List[RiskTrend]:
        with get_db_session() as session:
            repo = TrendRepository(session)
            return repo.get_project_trends(project_id, period_type)

trend_service = TrendService()
