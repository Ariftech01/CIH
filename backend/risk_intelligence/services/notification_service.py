from typing import List
from backend.database.session import get_db_session
from backend.risk_intelligence.repositories.notification_repository import NotificationRepository
from backend.risk_intelligence.models.notification_log import NotificationLog

class NotificationService:
    def get_pending_alerts(self, project_id: str) -> List[NotificationLog]:
        with get_db_session() as session:
            repo = NotificationRepository(session)
            return repo.get_pending_notifications(project_id)

notification_service = NotificationService()
