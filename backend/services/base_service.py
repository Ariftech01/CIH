from typing import Generic, TypeVar, List, Optional, Dict, Any
from backend.repositories.base_repository import BaseRepository
from backend.database.session import get_db_session

T = TypeVar("T")

class BaseService(Generic[T]):
    """
    Base Service Layer providing transaction safety and business operation wrappers around repositories.
    """
    def __init__(self, repo_cls: type):
        self.repo_cls = repo_cls

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        with get_db_session() as session:
            repo = self.repo_cls(session)
            return repo.get_all(skip=skip, limit=limit)

    def get_by_id(self, id_val: str) -> Optional[Any]:
        with get_db_session() as session:
            repo = self.repo_cls(session)
            return repo.get_by_id(id_val)

    def soft_delete(self, id_val: str) -> bool:
        with get_db_session() as session:
            repo = self.repo_cls(session)
            return repo.soft_delete(id_val)
