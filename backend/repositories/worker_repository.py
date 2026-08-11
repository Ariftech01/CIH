from typing import List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from backend.models.worker import Worker
from backend.repositories.base_repository import BaseRepository

class WorkerRepository(BaseRepository[Worker]):
    def __init__(self, session: Session):
        super().__init__(Worker, session)

    def get_by_project(self, project_id: str) -> List[Worker]:
        stmt = select(Worker).where(Worker.project_id == project_id, Worker.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_active_workers(self, project_id: str = None) -> List[Worker]:
        stmt = select(Worker).where(Worker.status == "ACTIVE", Worker.is_deleted == False)
        if project_id:
            stmt = stmt.where(Worker.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())

    def get_worker_summary(self, project_id: str) -> Dict[str, Any]:
        stmt = select(
            func.count(Worker.id).label("total_workers"),
            func.sum(Worker.daily_wage).label("total_daily_wage")
        ).where(Worker.project_id == project_id, Worker.is_deleted == False)
        res = self.session.execute(stmt).one_or_none()
        return {
            "total_workers": res.total_workers if res else 0,
            "total_daily_wage": float(res.total_daily_wage or 0.0) if res else 0.0
        }
