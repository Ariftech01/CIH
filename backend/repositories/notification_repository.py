from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.models.notification import Notification
from backend.repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session: Session):
        super().__init__(Notification, session)

    def get_unread(self, user_id: str = None) -> List[Notification]:
        stmt = select(Notification).where(Notification.is_read == False, Notification.is_deleted == False)
        if user_id:
            stmt = stmt.where(Notification.user_id == user_id)
        stmt = stmt.order_by(desc(Notification.timestamp))
        return list(self.session.execute(stmt).scalars().all())

    def mark_all_read(self, user_id: str = None) -> int:
        unread = self.get_unread(user_id)
        for n in unread:
            n.is_read = True
        self.session.flush()
        return len(unread)
