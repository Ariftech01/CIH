from typing import List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.safety_repository import SafetyAssessmentRepository
from backend.risk_intelligence.models.safety_assessment import SafetyAssessment

class SafetyService:
    def get_safety_history(self, project_id: str) -> List[SafetyAssessment]:
        with get_db_session() as session:
            repo = SafetyAssessmentRepository(session)
            return repo.get_by_project(project_id)

safety_service = SafetyService()
