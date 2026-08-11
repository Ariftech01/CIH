from datetime import date
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class TaskBase(BaseSchema):
    task_name: str
    task_category: Optional[str] = "General Construction"
    description: Optional[str] = None
    status: str = "PENDING"
    priority: str = "MEDIUM"
    due_date: Optional[date] = None
    completion_percentage: int = 0
    assigned_to: Optional[str] = None

class TaskCreate(TaskBase):
    project_id: str
    building_id: Optional[str] = None
    floor_id: Optional[str] = None
    parent_task_id: Optional[str] = None

class TaskUpdate(BaseSchema):
    task_name: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    completion_percentage: Optional[int] = None
    assigned_to: Optional[str] = None

class TaskResponse(TaskBase, AuditSchema):
    project_id: str
    building_id: Optional[str] = None
    floor_id: Optional[str] = None
    parent_task_id: Optional[str] = None
