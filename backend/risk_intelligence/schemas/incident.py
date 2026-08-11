from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class IncidentCreate(BaseModel):
    project_id: str
    worker_id: Optional[str] = None
    equipment_id: Optional[str] = None
    incident_type: str
    severity: str = "MEDIUM"
    title: str
    description: str
    location: Optional[str] = None
    financial_impact: float = 0.0
    corrective_action: Optional[str] = None

class IncidentResponse(BaseModel):
    id: str
    project_id: str
    worker_id: Optional[str] = None
    equipment_id: Optional[str] = None
    incident_type: str
    severity: str
    title: str
    description: str
    location: Optional[str] = None
    incident_date: datetime
    status: str
    financial_impact: float
    corrective_action: Optional[str] = None
    attachment_ref: Optional[str] = None

    class Config:
        from_attributes = True
