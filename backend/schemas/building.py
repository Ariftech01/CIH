from typing import Optional
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class BuildingBase(BaseSchema):
    building_name: str = Field(..., min_length=1, max_length=100)
    building_type: Optional[str] = "Residential"
    number_of_floors: int = Field(default=1, ge=1)
    total_area: float = Field(default=0.0, ge=0)
    units: Optional[str] = "sqm"

class BuildingCreate(BuildingBase):
    project_id: str

class BuildingUpdate(BaseSchema):
    building_name: Optional[str] = None
    building_type: Optional[str] = None
    number_of_floors: Optional[int] = Field(default=None, ge=1)
    total_area: Optional[float] = Field(default=None, ge=0)
    units: Optional[str] = None

class BuildingResponse(BuildingBase, AuditSchema):
    project_id: str
