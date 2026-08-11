from typing import Optional
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class RoomBase(BaseSchema):
    room_name: str = Field(..., min_length=1, max_length=100)
    room_type: Optional[str] = "Bedroom"
    length: float = Field(default=4.0, gt=0)
    width: float = Field(default=4.0, gt=0)
    height: float = Field(default=3.0, gt=0)
    area: float = Field(default=16.0, ge=0)
    perimeter: float = Field(default=16.0, ge=0)
    volume: float = Field(default=48.0, ge=0)
    wall_thickness: float = Field(default=0.23, gt=0)

class RoomCreate(RoomBase):
    floor_id: str

class RoomUpdate(BaseSchema):
    room_name: Optional[str] = None
    room_type: Optional[str] = None
    length: Optional[float] = Field(default=None, gt=0)
    width: Optional[float] = Field(default=None, gt=0)
    height: Optional[float] = Field(default=None, gt=0)
    area: Optional[float] = Field(default=None, ge=0)
    perimeter: Optional[float] = Field(default=None, ge=0)
    volume: Optional[float] = Field(default=None, ge=0)
    wall_thickness: Optional[float] = Field(default=None, gt=0)

class RoomResponse(RoomBase, AuditSchema):
    floor_id: str
