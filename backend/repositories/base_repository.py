from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy import select, update, func, or_, desc, asc
from sqlalchemy.orm import Session
from backend.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Generic Repository implementation providing robust CRUD, pagination,
    filtering, searching, soft deletion, and count operations using SQLAlchemy 2.x.
    """
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        self.session.flush()
        return db_obj

    def get_by_id(self, id_val: str, include_deleted: bool = False) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id_val)
        if not include_deleted and hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        include_deleted: bool = False,
        order_by_col: str = "created_at",
        descending: bool = True
    ) -> List[ModelType]:
        stmt = select(self.model)
        if not include_deleted and hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
        
        if hasattr(self.model, order_by_col):
            col_attr = getattr(self.model, order_by_col)
            stmt = stmt.order_by(desc(col_attr) if descending else asc(col_attr))

        stmt = stmt.offset(skip).limit(limit)
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def update(self, id_val: str, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        db_obj = self.get_by_id(id_val)
        if not db_obj:
            return None
        
        for key, value in obj_in.items():
            if hasattr(db_obj, key) and value is not None:
                setattr(db_obj, key, value)
        
        self.session.flush()
        return db_obj

    def soft_delete(self, id_val: str) -> bool:
        db_obj = self.get_by_id(id_val)
        if not db_obj:
            return False
        if hasattr(db_obj, "is_deleted"):
            db_obj.is_deleted = True
            db_obj.is_active = False
            self.session.flush()
            return True
        return False

    def restore(self, id_val: str) -> bool:
        db_obj = self.get_by_id(id_val, include_deleted=True)
        if not db_obj:
            return False
        if hasattr(db_obj, "is_deleted"):
            db_obj.is_deleted = False
            db_obj.is_active = True
            self.session.flush()
            return True
        return False

    def exists(self, id_val: str) -> bool:
        return self.get_by_id(id_val) is not None

    def count(self, include_deleted: bool = False, filters: Dict[str, Any] = None) -> int:
        stmt = select(func.count()).select_from(self.model)
        if not include_deleted and hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
        
        if filters:
            for key, val in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == val)

        result = self.session.execute(stmt)
        return result.scalar() or 0

    def filter(self, include_deleted: bool = False, **kwargs) -> List[ModelType]:
        stmt = select(self.model)
        if not include_deleted and hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
        
        for key, val in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == val)

        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def search(self, search_field: str, query_str: str, limit: int = 50) -> List[ModelType]:
        stmt = select(self.model)
        if hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
        
        if hasattr(self.model, search_field):
            col_attr = getattr(self.model, search_field)
            stmt = stmt.where(col_attr.ilike(f"%{query_str}%"))

        stmt = stmt.limit(limit)
        result = self.session.execute(stmt)
        return list(result.scalars().all())
