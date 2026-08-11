from typing import Optional, List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.models.cost_estimation import CostEstimation
from backend.repositories.base_repository import BaseRepository

class CostEstimationRepository(BaseRepository[CostEstimation]):
    def __init__(self, session: Session):
        super().__init__(CostEstimation, session)

    def get_latest_by_project(self, project_id: str) -> Optional[CostEstimation]:
        stmt = (
            select(CostEstimation)
            .where(CostEstimation.project_id == project_id, CostEstimation.is_deleted == False)
            .order_by(desc(CostEstimation.calculated_date))
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_history_by_project(self, project_id: str) -> List[CostEstimation]:
        stmt = (
            select(CostEstimation)
            .where(CostEstimation.project_id == project_id, CostEstimation.is_deleted == False)
            .order_by(desc(CostEstimation.calculated_date))
        )
        return list(self.session.execute(stmt).scalars().all())
