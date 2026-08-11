from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.audit_record import AuditRecord

class AuditRepository(BaseRepository[AuditRecord]):
    def __init__(self, session: Session):
        super().__init__(AuditRecord, session)

    def get_by_project(self, project_id: str, limit: int = 100) -> List[AuditRecord]:
        stmt = (
            select(AuditRecord)
            .where(AuditRecord.project_id == project_id)
            .order_by(desc(AuditRecord.timestamp))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())
