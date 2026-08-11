from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username, User.is_deleted == False)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email, User.is_deleted == False)
        return self.session.execute(stmt).scalar_one_or_none()

    def update_last_login(self, user_id: str) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            self.session.flush()
        return user
