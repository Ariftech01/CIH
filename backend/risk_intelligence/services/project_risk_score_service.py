from typing import List, Optional
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.project_risk_score_repository import ProjectRiskScoreRepository
from backend.risk_intelligence.models.project_risk_score import ProjectRiskScore

class ProjectRiskScoreService:
    def get_by_assessment(self, assessment_id: str) -> List[ProjectRiskScore]:
        with get_db_session() as session:
            repo = ProjectRiskScoreRepository(session)
            return repo.get_by_assessment(assessment_id)

    def get_latest_category_score(self, project_id: str, category: str) -> Optional[ProjectRiskScore]:
        with get_db_session() as session:
            repo = ProjectRiskScoreRepository(session)
            return repo.get_latest_by_category(project_id, category)

project_risk_score_service = ProjectRiskScoreService()
