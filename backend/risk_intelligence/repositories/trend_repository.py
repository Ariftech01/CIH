from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.risk_trend import RiskTrend

class TrendRepository(BaseRepository[RiskTrend]):
    def __init__(self, session: Session):
        super().__init__(RiskTrend, session)

    def get_project_trends(self, project_id: str, period_type: str = "WEEKLY") -> List[RiskTrend]:
        stmt = (
            select(RiskTrend)
            .where(RiskTrend.project_id == project_id)
            .where(RiskTrend.period_type == period_type)
            .where(RiskTrend.is_deleted == False)
            .order_by(desc(RiskTrend.period_start))
        )
        return list(self.session.execute(stmt).scalars().all())
