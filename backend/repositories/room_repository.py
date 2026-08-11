from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.room import Room
from backend.repositories.base_repository import BaseRepository

class RoomRepository(BaseRepository[Room]):
    def __init__(self, session: Session):
        super().__init__(Room, session)

    def get_by_floor(self, floor_id: str) -> List[Room]:
        stmt = select(Room).where(Room.floor_id == floor_id, Room.is_deleted == False)
        return list(self.session.execute(stmt).scalars().all())

    def update_geometry(self, room_id: str, length: float, width: float, height: float) -> Optional[Room]:
        room = self.get_by_id(room_id)
        if room:
            room.length = length
            room.width = width
            room.height = height
            room.area = length * width
            room.perimeter = 2 * (length + width)
            room.volume = length * width * height
            self.session.flush()
        return room
