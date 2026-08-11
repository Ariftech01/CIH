from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.task import Task
from backend.repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: Session):
        super().__init__(Task, session)

    def get_by_project(self, project_id: str) -> List[Task]:
        stmt = select(Task).where(Task.project_id == project_id, Task.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_pending_tasks(self, project_id: str = None) -> List[Task]:
        stmt = select(Task).where(Task.status.in_(["PENDING", "IN_PROGRESS"]), Task.is_deleted == False)
        if project_id:
            stmt = stmt.where(Task.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())
