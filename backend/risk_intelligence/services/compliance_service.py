from typing import List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.compliance_repository import ComplianceAssessmentRepository
from backend.risk_intelligence.models.compliance_assessment import ComplianceAssessment

class ComplianceService:
    def get_open_violations(self, project_id: str) -> List[ComplianceAssessment]:
        with get_db_session() as session:
            repo = ComplianceAssessmentRepository(session)
            return repo.get_non_compliant_records(project_id)

compliance_service = ComplianceService()
