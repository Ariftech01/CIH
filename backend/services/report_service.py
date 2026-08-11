from typing import List
from backend.database.session import get_db_session
from backend.repositories.report_repository import ReportRepository
from backend.schemas.report import ReportCreate, ReportResponse

class ReportService:
    def create_report_entry(self, report_in: ReportCreate) -> ReportResponse:
        with get_db_session() as session:
            repo = ReportRepository(session)
            rep = repo.create(report_in.model_dump())
            return ReportResponse.model_validate(rep)

    def get_project_reports(self, project_id: str) -> List[ReportResponse]:
        with get_db_session() as session:
            repo = ReportRepository(session)
            reps = repo.get_by_project(project_id)
            return [ReportResponse.model_validate(r) for r in reps]

report_service = ReportService()
