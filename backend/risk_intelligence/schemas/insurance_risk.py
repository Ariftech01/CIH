from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class InsuranceObservation(BaseModel):
    observation_id: str
    source: str = "MANUAL_INSURANCE_RECORD"  # MANUAL_INSURANCE_RECORD, POLICY_SYSTEM, INCIDENT_LOG, PROVIDER_API, DIGITAL_CLAIM, ERP, WEATHER_API, IOT, COMPUTER_VISION
    incident_id: Optional[str] = None
    policy_ref: Optional[str] = None
    category: str  # PROPERTY_DAMAGE, EQUIPMENT, WORKER_COMPENSATION, THIRD_PARTY_LIABILITY, PUBLIC_LIABILITY, BUSINESS_INTERRUPTION, CLAIM_DOCUMENTATION
    severity: str = "LOW"  # INFORMATIONAL, LOW, MODERATE, HIGH, CRITICAL
    confidence: float = 1.0
    evidence: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class InsuranceHazard(BaseModel):
    hazard_id: str
    category: str
    title: str
    severity: str  # INFORMATIONAL, LOW, MODERATE, HIGH, CRITICAL
    description: str
    affected_asset: Optional[str] = None
    policy_ref: Optional[str] = "Commercial General Liability"
    business_justification: str
    evidence: Optional[str] = None

class InsuranceFinding(BaseModel):
    category: str
    title: str
    description: str
    severity: str  # INFORMATIONAL, LOW, MODERATE, HIGH, CRITICAL
    policy_ref: Optional[str] = "Commercial General Liability"
    affected_asset: Optional[str] = None
    evidence: Optional[str] = None
    suggested_action: str
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class InsuranceMonitoringSession(BaseModel):
    session_id: str
    project_id: str
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow)
    policies_evaluated_count: int = 0
    incidents_reviewed_count: int = 0
    claims_reviewed_count: int = 0
    assets_evaluated_count: int = 0
    insurance_score: float = 0.0
    findings: List[InsuranceFinding] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class InsuranceState(BaseModel):
    project_id: str
    current_insurance_score: float = 0.0
    health_status: str = "HEALTHY"  # HEALTHY, ELEVATED_EXPOSURE, CRITICAL_EXPOSURE
    active_claims_count: int = 0
    critical_exposure_count: int = 0
    claim_readiness_status: str = "CLAIM_READY"  # CLAIM_READY, DEFICIENT_DOCUMENTATION, CRITICAL_DOC_DEFICIENCY
    exposure_trend: str = "STABLE"  # IMPROVING, STABLE, DETERIORATING
    last_session_id: Optional[str] = None
    last_evaluated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectInsuranceProfile(BaseModel):
    project_id: str
    project_name: str = "Unknown Project"
    policy_coverage_rate: float = 100.0
    claim_readiness_rate: float = 100.0
    asset_protection_rate: float = 100.0
    liability_exposure_index: float = 0.0
    insurance_score: float = 100.0

class AssetInsuranceProfile(BaseModel):
    asset_id: str
    asset_name: str = "Construction Asset"
    asset_category: str = "Heavy Machinery"
    replacement_value: float = 0.0
    coverage_status: str = "COVERED"  # COVERED, UNINSURED, EXCLUDED, RENEWAL_DUE
    incident_history_count: int = 0
    insurance_score: float = 100.0

class InsuranceChangeRecord(BaseModel):
    project_id: str
    previous_score: float
    current_score: float
    score_delta: float
    new_findings_count: int
    resolved_findings_count: int
    movement_summary: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class InsuranceMetric(BaseModel):
    metric_name: str
    metric_value: float
    category: str
    status: str
    description: str
