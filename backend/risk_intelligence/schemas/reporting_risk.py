from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ReportSection(BaseModel):
    title: str
    content: str
    section_type: str = "TEXT"  # TEXT, SUMMARY, TABLE, METRICS, HAZARDS, RECOMMENDATIONS
    order: int = 1
    subsections: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReportExecutiveSummary(BaseModel):
    project_id: str
    project_name: str = "Unknown Project"
    overall_risk_score: float = 0.0
    risk_level: str = "LOW"
    health_status: str = "HEALTHY"
    key_highlights: List[str] = Field(default_factory=list)
    critical_findings_count: int = 0
    top_recommendations: List[Dict[str, Any]] = Field(default_factory=list)

class EnterpriseReport(BaseModel):
    report_id: str
    project_id: str
    report_type: str = "EXECUTIVE_RISK_SUMMARY"  # EXECUTIVE_RISK_SUMMARY, DAILY_SITE, SAFETY, COMPLIANCE, INSURANCE, PROJECT_HEALTH, FULL_CRI
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    executive_summary: ReportExecutiveSummary
    sections: List[ReportSection] = Field(default_factory=list)
    template_version: str = "1.0.0"
    report_version: str = "1.0.0"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReportGenerationSession(BaseModel):
    session_id: str
    project_id: str
    report_id: str
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    report_type: str = "EXECUTIVE_RISK_SUMMARY"
    included_agents: List[str] = Field(default_factory=list)
    included_sections: List[str] = Field(default_factory=list)
    generation_duration_ms: float = 0.0
    status: str = "GENERATED"  # DRAFT, GENERATED, VALIDATED, APPROVED, PUBLISHED, ARCHIVED
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ReportState(BaseModel):
    project_id: str
    latest_report_id: Optional[str] = None
    health_status: str = "HEALTHY"
    quality_status: str = "PASSED"  # PASSED, WARNING, FAILED
    published_count: int = 0
    archived_count: int = 0
    last_generated_at: datetime = Field(default_factory=datetime.utcnow)

class ReportChangeRecord(BaseModel):
    project_id: str
    previous_report_id: Optional[str] = None
    current_report_id: str
    sections_changed_count: int = 0
    movement_summary: str = "New report version generated"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ReportMetric(BaseModel):
    metric_name: str
    metric_value: float
    category: str
    status: str
    description: str

class ReportExportRequest(BaseModel):
    export_id: str
    report_id: str
    format: str = "JSON"  # JSON, PDF, EXCEL, WORD, POWERPOINT, POWER_BI, SHAREPOINT, EMAIL, TEAMS
    destination: str = "DASHBOARD"
    classification: str = "INTERNAL"  # PUBLIC, INTERNAL, CONFIDENTIAL, EXECUTIVE_ONLY, AUDIT
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
