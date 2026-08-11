from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.executive_summary import ExecutiveSummary

class ExecutiveSummaryRepository(BaseRepository[ExecutiveSummary]):
    def __init__(self, session: Session):
        super().__init__(ExecutiveSummary, session)

    def get_latest_by_project(self, project_id: str) -> Optional[ExecutiveSummary]:
        stmt = (
            select(ExecutiveSummary)
            .where(ExecutiveSummary.project_id == project_id)
            .where(ExecutiveSummary.is_deleted == False)
            .order_by(desc(ExecutiveSummary.generated_at))
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()
