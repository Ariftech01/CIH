from typing import Optional
from pydantic import Field
from backend.schemas.common import BaseSchema, AuditSchema

class WorkerBase(BaseSchema):
    worker_name: str = Field(..., min_length=1, max_length=100)
    designation: Optional[str] = "Mason"
    contact: Optional[str] = None
    daily_wage: float = Field(default=0.0, ge=0)
    attendance: Optional[str] = "PRESENT"
    assigned_task: Optional[str] = None
    status: str = "ACTIVE"

class WorkerCreate(WorkerBase):
    project_id: str

class WorkerUpdate(BaseSchema):
    worker_name: Optional[str] = None
    designation: Optional[str] = None
    contact: Optional[str] = None
    daily_wage: Optional[float] = Field(default=None, ge=0)
    attendance: Optional[str] = None
    assigned_task: Optional[str] = None
    status: Optional[str] = None

class WorkerResponse(WorkerBase, AuditSchema):
    project_id: str
