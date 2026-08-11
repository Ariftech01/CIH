from typing import List
from backend.database.session import get_db_session
from backend.repositories.notification_repository import NotificationRepository
from backend.schemas.notification import NotificationCreate, NotificationResponse

class NotificationService:
    def create_notification(self, notif_in: NotificationCreate) -> NotificationResponse:
        with get_db_session() as session:
            repo = NotificationRepository(session)
            n = repo.create(notif_in.model_dump())
            return NotificationResponse.model_validate(n)

    def get_unread_notifications(self, user_id: str = None) -> List[NotificationResponse]:
        with get_db_session() as session:
            repo = NotificationRepository(session)
            notifs = repo.get_unread(user_id)
            return [NotificationResponse.model_validate(n) for n in notifs]

notification_service = NotificationService()
