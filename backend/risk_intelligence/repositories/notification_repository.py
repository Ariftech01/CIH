from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.notification_log import NotificationLog

class NotificationRepository(BaseRepository[NotificationLog]):
    def __init__(self, session: Session):
        super().__init__(NotificationLog, session)

    def get_pending_notifications(self, project_id: str) -> List[NotificationLog]:
        stmt = (
            select(NotificationLog)
            .where(NotificationLog.project_id == project_id)
            .where(NotificationLog.is_delivered == False)
            .where(NotificationLog.is_deleted == False)
            .order_by(desc(NotificationLog.created_at))
        )
        return list(self.session.execute(stmt).scalars().all())
