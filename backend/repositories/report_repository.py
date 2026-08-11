from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.models.report import Report
from backend.repositories.base_repository import BaseRepository

class ReportRepository(BaseRepository[Report]):
    def __init__(self, session: Session):
        super().__init__(Report, session)

    def get_by_project(self, project_id: str) -> List[Report]:
        stmt = (
            select(Report)
            .where(Report.project_id == project_id, Report.is_deleted == False)
            .order_by(desc(Report.generated_date))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_type(self, report_type: str) -> List[Report]:
        stmt = select(Report).where(Report.report_type == report_type, Report.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())
