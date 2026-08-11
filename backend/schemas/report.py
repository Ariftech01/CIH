from datetime import datetime
from typing import Optional
from backend.schemas.common import BaseSchema, AuditSchema

class ReportBase(BaseSchema):
    report_name: str
    report_type: str = "SUMMARY"
    generated_by: Optional[str] = None
    generated_date: datetime = Field(default_factory=datetime.utcnow) if 'Field' in globals() else None
    file_path: Optional[str] = None

class ReportCreate(BaseSchema):
    project_id: str
    report_name: str
    report_type: str = "SUMMARY"
    generated_by: Optional[str] = None
    file_path: Optional[str] = None

class ReportResponse(AuditSchema):
    project_id: str
    report_name: str
    report_type: str
    generated_by: Optional[str] = None
    generated_date: datetime
    file_path: Optional[str] = None
