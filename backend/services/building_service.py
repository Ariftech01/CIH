from typing import List, Optional, Dict, Any
from backend.database.session import get_db_session
from backend.repositories.building_repository import BuildingRepository
from backend.repositories.room_repository import RoomRepository
from backend.schemas.building import BuildingCreate, BuildingResponse
from backend.schemas.floor import FloorCreate, FloorResponse
from backend.schemas.room import RoomCreate, RoomResponse
from backend.repositories.base_repository import BaseRepository
from backend.models.floor import Floor
from backend.utils.exceptions import BuildingNotFound

class BuildingService:
    def create_building(self, building_in: BuildingCreate) -> BuildingResponse:
        with get_db_session() as session:
            repo = BuildingRepository(session)
            bld = repo.create(building_in.model_dump())
            return BuildingResponse.model_validate(bld)

    def get_building(self, building_id: str) -> BuildingResponse:
        with get_db_session() as session:
            repo = BuildingRepository(session)
            bld = repo.get_by_id(building_id)
            if not bld:
                raise BuildingNotFound(building_id)
            return BuildingResponse.model_validate(bld)

    def get_project_buildings(self, project_id: str) -> List[BuildingResponse]:
        with get_db_session() as session:
            repo = BuildingRepository(session)
            buildings = repo.get_by_project(project_id)
            return [BuildingResponse.model_validate(b) for b in buildings]

    def add_floor(self, building_id: str, floor_in: FloorCreate) -> FloorResponse:
        with get_db_session() as session:
            floor_repo = BaseRepository(Floor, session)
            flr = floor_repo.create(floor_in.model_dump())
            return FloorResponse.model_validate(flr)

    def add_room(self, room_in: RoomCreate) -> RoomResponse:
        with get_db_session() as session:
            room_repo = RoomRepository(session)
            data = room_in.model_dump()
            data["area"] = room_in.length * room_in.width
            data["perimeter"] = 2 * (room_in.length + room_in.width)
            data["volume"] = room_in.length * room_in.width * room_in.height
            rm = room_repo.create(data)
            return RoomResponse.model_validate(rm)

building_service = BuildingService()
