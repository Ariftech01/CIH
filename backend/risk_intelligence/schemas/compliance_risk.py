from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ComplianceObservation(BaseModel):
    observation_id: str
    source: str = "MANUAL_COMPLIANCE_RECORD"  # MANUAL_COMPLIANCE_RECORD, PERMIT_SYSTEM, INSPECTION_FORM, GOVT_API, OCR_DOC, DIGITAL_TWIN, BIM
    permit_id: Optional[str] = None
    category: str  # PERMIT, LICENSE, INSPECTION, DOCUMENTATION, SAFETY_REGULATION, CERTIFICATION, POLICY
    severity: str = "MINOR"  # INFORMATIONAL, MINOR, MODERATE, MAJOR, CRITICAL
    confidence: float = 1.0
    evidence: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ComplianceHazard(BaseModel):
    hazard_id: str
    category: str
    title: str
    severity: str  # INFORMATIONAL, MINOR, MODERATE, MAJOR, CRITICAL
    description: str
    regulation_ref: Optional[str] = "Building Code Regulations"
    business_justification: str
    evidence: Optional[str] = None

class ComplianceFinding(BaseModel):
    category: str
    title: str
    description: str
    severity: str  # INFORMATIONAL, MINOR, MODERATE, MAJOR, CRITICAL
    regulation_ref: Optional[str] = "Building Code Regulations"
    evidence: Optional[str] = None
    suggested_action: str
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ComplianceMonitoringSession(BaseModel):
    session_id: str
    project_id: str
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow)
    permits_evaluated_count: int = 0
    inspections_reviewed_count: int = 0
    documents_verified_count: int = 0
    certifications_validated_count: int = 0
    compliance_score: float = 0.0
    findings: List[ComplianceFinding] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GovernanceState(BaseModel):
    project_id: str
    current_compliance_score: float = 0.0
    health_status: str = "HEALTHY"  # HEALTHY, MINOR_NON_COMPLIANCE, CRITICAL_NON_COMPLIANCE
    active_violations_count: int = 0
    critical_violations_count: int = 0
    audit_readiness_status: str = "AUDIT_READY"  # AUDIT_READY, MINOR_DEFICIENCIES, CRITICAL_DEFICIENCIES
    regulatory_trend: str = "STABLE"  # IMPROVING, STABLE, DETERIORATING
    last_session_id: Optional[str] = None
    last_evaluated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectGovernanceProfile(BaseModel):
    project_id: str
    project_name: str = "Unknown Project"
    permit_compliance_rate: float = 100.0
    inspection_completion_rate: float = 100.0
    documentation_accuracy_rate: float = 100.0
    certification_validity_rate: float = 100.0
    audit_readiness_index: float = 100.0
    governance_maturity_level: str = "MATURE"  # INITIAL, DEVELOPING, MATURE, LEADING
    compliance_score: float = 100.0

class ContractorComplianceProfile(BaseModel):
    contractor_id: str
    contractor_name: str = "General Contractor"
    trade: str = "General Construction"
    permit_status: str = "COMPLIANT"
    violation_count: int = 0
    audit_performance_score: float = 100.0
    compliance_score: float = 100.0
    regulatory_trend: str = "STABLE"

class ComplianceChangeRecord(BaseModel):
    project_id: str
    previous_score: float
    current_score: float
    score_delta: float
    new_findings_count: int
    resolved_findings_count: int
    movement_summary: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ComplianceMetric(BaseModel):
    metric_name: str
    metric_value: float
    category: str
    status: str
    description: str
