from typing import List, Optional
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.incident_repository import IncidentRepository
from backend.risk_intelligence.models.incident_record import IncidentRecord

class IncidentService:
    def create_incident(
        self,
        project_id: str,
        incident_type: str,
        title: str,
        description: str,
        severity: str = "MEDIUM",
        worker_id: Optional[str] = None,
        equipment_id: Optional[str] = None,
        location: Optional[str] = None,
        financial_impact: float = 0.0
    ) -> IncidentRecord:
        with get_db_session() as session:
            repo = IncidentRepository(session)
            incident = IncidentRecord(
                project_id=project_id,
                incident_type=incident_type,
                title=title,
                description=description,
                severity=severity,
                worker_id=worker_id,
                equipment_id=equipment_id,
                location=location,
                financial_impact=financial_impact,
                status="OPEN"
            )
            session.add(incident)
            session.flush()
            return incident

    def get_open_incidents(self, project_id: str) -> List[IncidentRecord]:
        with get_db_session() as session:
            repo = IncidentRepository(session)
            return repo.get_open_incidents(project_id)

incident_service = IncidentService()
