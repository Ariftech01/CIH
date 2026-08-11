from datetime import date
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class SafetyInspectionBase(BaseSchema):
    inspection_date: date
    risk_level: str = "LOW"
    description: Optional[str] = None
    corrective_action: Optional[str] = None
    status: str = "OPEN"

class SafetyInspectionCreate(SafetyInspectionBase):
    project_id: str

class SafetyInspectionUpdate(BaseSchema):
    risk_level: Optional[str] = None
    description: Optional[str] = None
    corrective_action: Optional[str] = None
    status: Optional[str] = None

class SafetyInspectionResponse(SafetyInspectionBase, AuditSchema):
    project_id: str
