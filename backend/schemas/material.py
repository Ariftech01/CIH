from typing import Optional
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class MaterialBase(BaseSchema):
    material_name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = "General"
    unit: str = "pcs"
    quantity_required: float = Field(default=0.0, ge=0)
    quantity_available: float = Field(default=0.0, ge=0)
    supplier: Optional[str] = None
    unit_cost: float = Field(default=0.0, ge=0)
    total_cost: float = Field(default=0.0, ge=0)

class MaterialCreate(MaterialBase):
    project_id: str

class MaterialUpdate(BaseSchema):
    material_name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    quantity_required: Optional[float] = Field(default=None, ge=0)
    quantity_available: Optional[float] = Field(default=None, ge=0)
    supplier: Optional[str] = None
    unit_cost: Optional[float] = Field(default=None, ge=0)
    total_cost: Optional[float] = Field(default=None, ge=0)

class MaterialResponse(MaterialBase, AuditSchema):
    project_id: str
