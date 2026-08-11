from typing import List, Optional, Dict, Any
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.audit_repository import AuditRepository
from backend.risk_intelligence.models.audit_record import AuditRecord

class AuditService:
    def log_event(
        self,
        action: str,
        entity_type: str,
        project_id: Optional[str] = None,
        performed_by: Optional[str] = None,
        entity_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditRecord:
        with get_db_session() as session:
            repo = AuditRepository(session)
            return repo.log_audit(
                action=action,
                entity_type=entity_type,
                project_id=project_id,
                performed_by=performed_by,
                entity_id=entity_id,
                details=details
            )

    def get_audit_trail(self, project_id: str) -> List[AuditRecord]:
        with get_db_session() as session:
            repo = AuditRepository(session)
            return repo.get_by_project(project_id)

audit_service = AuditService()
