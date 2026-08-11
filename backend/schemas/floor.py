from typing import Optional
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class FloorBase(BaseSchema):
    floor_number: int
    floor_name: str = Field(..., min_length=1, max_length=100)
    floor_height: float = Field(default=3.0, gt=0)
    area: float = Field(default=0.0, ge=0)

class FloorCreate(FloorBase):
    building_id: str

class FloorUpdate(BaseSchema):
    floor_number: Optional[int] = None
    floor_name: Optional[str] = None
    floor_height: Optional[float] = Field(default=None, gt=0)
    area: Optional[float] = Field(default=None, ge=0)

class FloorResponse(FloorBase, AuditSchema):
    building_id: str
