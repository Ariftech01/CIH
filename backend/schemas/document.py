from datetime import datetime
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class DocumentCreate(BaseSchema):
    project_id: Optional[str] = None
    conversation_id: Optional[str] = None
    file_name: str
    file_type: Optional[str] = None
    file_size: int = 0
    storage_path: str

class DocumentResponse(AuditSchema):
    project_id: Optional[str] = None
    conversation_id: Optional[str] = None
    file_name: str
    file_type: Optional[str] = None
    file_size: int
    storage_path: str
    uploaded_at: datetime
