from typing import List, Optional
from backend.database.session import get_db_session
from backend.repositories.task_repository import TaskRepository
from backend.schemas.task import TaskCreate, TaskUpdate, TaskResponse

class TaskService:
    def create_task(self, task_in: TaskCreate) -> TaskResponse:
        with get_db_session() as session:
            repo = TaskRepository(session)
            t = repo.create(task_in.model_dump())
            return TaskResponse.model_validate(t)

    def get_project_tasks(self, project_id: str) -> List[TaskResponse]:
        with get_db_session() as session:
            repo = TaskRepository(session)
            tasks = repo.get_by_project(project_id)
            return [TaskResponse.model_validate(t) for t in tasks]

    def update_task(self, task_id: str, update_in: TaskUpdate) -> TaskResponse:
        with get_db_session() as session:
            repo = TaskRepository(session)
            data = {k: v for k, v in update_in.model_dump().items() if v is not None}
            t = repo.update(task_id, data)
            return TaskResponse.model_validate(t)

task_service = TaskService()
