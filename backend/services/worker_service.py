from typing import List, Dict, Any
from backend.database.session import get_db_session
from backend.repositories.worker_repository import WorkerRepository
from backend.schemas.worker import WorkerCreate, WorkerResponse

class WorkerService:
    def add_worker(self, worker_in: WorkerCreate) -> WorkerResponse:
        with get_db_session() as session:
            repo = WorkerRepository(session)
            w = repo.create(worker_in.model_dump())
            return WorkerResponse.model_validate(w)

    def get_project_workers(self, project_id: str) -> List[WorkerResponse]:
        with get_db_session() as session:
            repo = WorkerRepository(session)
            workers = repo.get_by_project(project_id)
            return [WorkerResponse.model_validate(w) for w in workers]

    def get_worker_summary(self, project_id: str) -> Dict[str, Any]:
        with get_db_session() as session:
            repo = WorkerRepository(session)
            return repo.get_worker_summary(project_id)

worker_service = WorkerService()
