from typing import Optional, List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.risk_assessment_repository import RiskAssessmentRepository
from backend.risk_intelligence.models.risk_assessment import RiskAssessment

class RiskAssessmentService:
    def create_assessment(self, project_id: str, assessment_type: str = "FULL") -> RiskAssessment:
        with get_db_session() as session:
            repo = RiskAssessmentRepository(session)
            assessment = RiskAssessment(
                project_id=project_id,
                assessment_type=assessment_type,
                overall_risk_score=0.0,
                risk_level="PENDING"
            )
            session.add(assessment)
            session.flush()
            return assessment

    def get_latest(self, project_id: str) -> Optional[RiskAssessment]:
        with get_db_session() as session:
            repo = RiskAssessmentRepository(session)
            return repo.get_latest_by_project(project_id)

    def get_history(self, project_id: str) -> List[RiskAssessment]:
        with get_db_session() as session:
            repo = RiskAssessmentRepository(session)
            return repo.get_project_history(project_id)

risk_assessment_service = RiskAssessmentService()
