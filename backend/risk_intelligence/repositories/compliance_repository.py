from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.compliance_assessment import ComplianceAssessment

class ComplianceAssessmentRepository(BaseRepository[ComplianceAssessment]):
    def __init__(self, session: Session):
        super().__init__(ComplianceAssessment, session)

    def get_non_compliant_records(self, project_id: str) -> List[ComplianceAssessment]:
        stmt = (
            select(ComplianceAssessment)
            .where(ComplianceAssessment.project_id == project_id)
            .where(ComplianceAssessment.compliance_status != "COMPLIANT")
            .where(ComplianceAssessment.is_deleted == False)
            .order_by(desc(ComplianceAssessment.checked_at))
        )
        return list(self.session.execute(stmt).scalars().all())
