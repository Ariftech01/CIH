from datetime import date
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class EquipmentBase(BaseSchema):
    equipment_name: str
    equipment_type: Optional[str] = "Heavy Duty"
    status: str = "OPERATIONAL"
    availability: Optional[str] = "AVAILABLE"
    maintenance_date: Optional[date] = None
    operator: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    project_id: str

class EquipmentUpdate(BaseSchema):
    equipment_name: Optional[str] = None
    equipment_type: Optional[str] = None
    status: Optional[str] = None
    availability: Optional[str] = None
    maintenance_date: Optional[date] = None
    operator: Optional[str] = None

class EquipmentResponse(EquipmentBase, AuditSchema):
    project_id: str
