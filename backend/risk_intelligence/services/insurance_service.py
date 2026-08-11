from typing import List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.insurance_repository import InsuranceAssessmentRepository
from backend.risk_intelligence.models.insurance_assessment import InsuranceAssessment

class InsuranceService:
    def get_insurance_history(self, project_id: str) -> List[InsuranceAssessment]:
        with get_db_session() as session:
            repo = InsuranceAssessmentRepository(session)
            return repo.get_by_project(project_id)

insurance_service = InsuranceService()
