from typing import Optional
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.risk_snapshot_repository import RiskSnapshotRepository
from backend.risk_intelligence.models.risk_snapshot import RiskSnapshot

class SnapshotService:
    def get_latest_snapshot(self, project_id: str) -> Optional[RiskSnapshot]:
        with get_db_session() as session:
            repo = RiskSnapshotRepository(session)
            return repo.get_latest_snapshot(project_id)

snapshot_service = SnapshotService()
