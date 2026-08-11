from datetime import datetime
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class NotificationCreate(BaseSchema):
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    notification_type: str = "INFO"
    title: str
    message: str

class NotificationResponse(AuditSchema):
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    notification_type: str
    title: str
    message: str
    is_read: bool
    timestamp: datetime
