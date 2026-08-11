from datetime import datetime
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class WorkflowStateBase(BaseSchema):
    current_stage: str = "DRAFT"
    current_status: str = "Project Created"
    building_designed: bool = False
    cost_estimated: bool = False
    materials_prepared: bool = False
    workers_assigned: bool = False
    equipment_allocated: bool = False
    safety_inspected: bool = False
    progress_updated: bool = False
    reports_generated: bool = False
    ai_reviewed: bool = False
    predictions_generated: bool = False

class WorkflowStateResponse(WorkflowStateBase, AuditSchema):
    project_id: str
    last_transition_at: datetime

class WorkflowHistoryCreate(BaseSchema):
    project_id: str
    from_stage: str
    to_stage: str
    action: str
    performed_by: Optional[str] = None
    notes: Optional[str] = None

class WorkflowHistoryResponse(AuditSchema):
    project_id: str
    from_stage: str
    to_stage: str
    action: str
    performed_by: Optional[str] = None
    timestamp: datetime
    notes: Optional[str] = None
