from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.incident_record import IncidentRecord

class IncidentRepository(BaseRepository[IncidentRecord]):
    def __init__(self, session: Session):
        super().__init__(IncidentRecord, session)

    def get_open_incidents(self, project_id: str) -> List[IncidentRecord]:
        stmt = (
            select(IncidentRecord)
            .where(IncidentRecord.project_id == project_id)
            .where(IncidentRecord.status == "OPEN")
            .where(IncidentRecord.is_deleted == False)
            .order_by(desc(IncidentRecord.incident_date))
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_by_severity(self, project_id: str, severity: str) -> List[IncidentRecord]:
        stmt = (
            select(IncidentRecord)
            .where(IncidentRecord.project_id == project_id)
            .where(IncidentRecord.severity == severity)
            .where(IncidentRecord.is_deleted == False)
            .order_by(desc(IncidentRecord.incident_date))
        )
        return list(self.session.execute(stmt).scalars().all())
