from datetime import datetime
from typing import Optional
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class CostEstimationBase(BaseSchema):
    estimated_material_cost: float = Field(default=0.0, ge=0)
    estimated_labour_cost: float = Field(default=0.0, ge=0)
    estimated_equipment_cost: float = Field(default=0.0, ge=0)
    estimated_total_cost: float = Field(default=0.0, ge=0)
    currency: str = "USD"
    calculated_date: datetime = Field(default_factory=datetime.utcnow)

class CostEstimationCreate(CostEstimationBase):
    project_id: str

class CostEstimationResponse(CostEstimationBase, AuditSchema):
    project_id: str
