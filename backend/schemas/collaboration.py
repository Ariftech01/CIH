from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class ProjectMemberCreate(BaseSchema):
    project_id: str
    user_id: str
    project_role: str = "PROJECT_MANAGER"

class ProjectMemberResponse(AuditSchema):
    project_id: str
    user_id: str
    project_role: str
