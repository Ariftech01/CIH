from typing import List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from backend.models.equipment import Equipment
from backend.repositories.base_repository import BaseRepository

class EquipmentRepository(BaseRepository[Equipment]):
    def __init__(self, session: Session):
        super().__init__(Equipment, session)

    def get_by_project(self, project_id: str) -> List[Equipment]:
        stmt = select(Equipment).where(Equipment.project_id == project_id, Equipment.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_operational_equipment(self, project_id: str = None) -> List[Equipment]:
        stmt = select(Equipment).where(Equipment.status == "OPERATIONAL", Equipment.is_deleted == False)
        if project_id:
            stmt = stmt.where(Equipment.project_id == project_id)
        return list(self.session.execute(stmt).scalars().all())

    def get_equipment_summary(self, project_id: str) -> Dict[str, Any]:
        stmt = select(
            func.count(Equipment.id).label("total_equipment")
        ).where(Equipment.project_id == project_id, Equipment.is_deleted == False)
        res = self.session.execute(stmt).one_or_none()
        return {"total_equipment": res.total_equipment if res else 0}
