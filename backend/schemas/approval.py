from datetime import datetime
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class ApprovalBase(BaseSchema):
    approval_type: str
    title: str
    description: Optional[str] = None

class ApprovalCreate(ApprovalBase):
    project_id: str
    requested_by: Optional[str] = None

class ApprovalUpdate(BaseSchema):
    status: str # APPROVED, REJECTED, UNDER_REVIEW
    approved_by: Optional[str] = None
    comments: Optional[str] = None

class ApprovalResponse(ApprovalBase, AuditSchema):
    project_id: str
    status: str
    requested_by: Optional[str] = None
    approved_by: Optional[str] = None
    approval_time: Optional[datetime] = None
    comments: Optional[str] = None
