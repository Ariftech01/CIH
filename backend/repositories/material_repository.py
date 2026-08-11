from typing import List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from backend.models.material import Material
from backend.repositories.base_repository import BaseRepository

class MaterialRepository(BaseRepository[Material]):
    def __init__(self, session: Session):
        super().__init__(Material, session)

    def get_by_project(self, project_id: str) -> List[Material]:
        stmt = select(Material).where(Material.project_id == project_id, Material.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_low_stock(self, project_id: str = None) -> List[Material]:
        stmt = select(Material).where(
            Material.is_deleted == False,
            Material.quantity_available < Material.quantity_required
        )
        if project_id:
            stmt = stmt.where(Material.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())

    def get_inventory_summary(self, project_id: str) -> Dict[str, Any]:
        stmt = select(
            func.count(Material.id).label("total_items"),
            func.sum(Material.total_cost).label("total_value"),
            func.sum(Material.quantity_available).label("total_available"),
            func.sum(Material.quantity_required).label("total_required")
        ).where(Material.project_id == project_id, Material.is_deleted == False)
        res = self.session.execute(stmt).one_or_none()
        if res:
            return {
                "total_items": res.total_items or 0,
                "total_value": float(res.total_value or 0.0),
                "total_available": float(res.total_available or 0.0),
                "total_required": float(res.total_required or 0.0)
            }
        return {"total_items": 0, "total_value": 0.0, "total_available": 0.0, "total_required": 0.0}
