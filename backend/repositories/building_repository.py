from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from backend.models.building import Building
from backend.models.floor import Floor
from backend.repositories.base_repository import BaseRepository

class BuildingRepository(BaseRepository[Building]):
    def __init__(self, session: Session):
        super().__init__(Building, session)

    def get_by_project(self, project_id: str) -> List[Building]:
        stmt = select(Building).where(Building.project_id == project_id, Building.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def get_building_hierarchy(self, building_id: str) -> Optional[Building]:
        stmt = (
            select(Building)
            .where(Building.id == building_id, Building.is_deleted == False)
            .options(selectinload(Building.floors).selectinload(Floor.rooms))
        )
        return self.session.execute(stmt).scalar_one_or_none()
