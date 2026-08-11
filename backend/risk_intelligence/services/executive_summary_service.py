from typing import Optional
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.executive_summary_repository import ExecutiveSummaryRepository
from backend.risk_intelligence.models.executive_summary import ExecutiveSummary

class ExecutiveSummaryService:
    def get_latest_summary(self, project_id: str) -> Optional[ExecutiveSummary]:
        with get_db_session() as session:
            repo = ExecutiveSummaryRepository(session)
            return repo.get_latest_by_project(project_id)

executive_summary_service = ExecutiveSummaryService()
