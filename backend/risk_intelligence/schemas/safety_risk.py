from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SafetyObservation(BaseModel):
    observation_id: str
    source: str = "MANUAL_OBSERVATION"  # MANUAL_OBSERVATION, FORM, CCTV, COMPUTER_VISION, WEARABLE, BLE, RFID, GPS, DIGITAL_TWIN
    worker_id: Optional[str] = None
    location: Optional[str] = "General Work Zone"
    category: str  # PPE, UNSAFE_BEHAVIOUR, HAZARD_EXPOSURE, RESTRICTED_AREA, HIGH_RISK_ACTIVITY
    severity: str = "LOW"  # INFORMATIONAL, LOW, MODERATE, HIGH, CRITICAL
    confidence: float = 1.0
    evidence: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SafetyHazard(BaseModel):
    hazard_id: str
    category: str
    title: str
    severity: str  # INFORMATIONAL, LOW, MODERATE, HIGH, CRITICAL
    description: str
    location: Optional[str] = None
    worker_ref: Optional[str] = None
    business_justification: str
    evidence: Optional[str] = None

class SafetyFinding(BaseModel):
    category: str
    title: str
    description: str
    severity: str  # INFORMATIONAL, LOW, MODERATE, HIGH, CRITICAL
    location: Optional[str] = None
    worker_ref: Optional[str] = None
    evidence: Optional[str] = None
    suggested_action: str
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SafetyMonitoringSession(BaseModel):
    session_id: str
    project_id: str
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow)
    workers_evaluated_count: int = 0
    observed_conditions_count: int = 0
    hazards_detected_count: int = 0
    safety_score: float = 0.0
    findings: List[SafetyFinding] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkforceSafetyState(BaseModel):
    project_id: str
    current_safety_score: float = 0.0
    health_status: str = "HEALTHY"  # HEALTHY, ELEVATED_RISK, CRITICAL
    active_hazards_count: int = 0
    critical_hazards_count: int = 0
    high_risk_workers_count: int = 0
    high_risk_zones_count: int = 0
    safety_trend: str = "STABLE"  # IMPROVING, STABLE, DETERIORATING
    last_session_id: Optional[str] = None
    last_evaluated_at: datetime = Field(default_factory=datetime.utcnow)

class WorkerSafetyProfile(BaseModel):
    worker_id: str
    worker_name: str = "Unknown Worker"
    trade: str = "General Labour"
    safety_history_count: int = 0
    ppe_compliance_rate: float = 100.0
    near_miss_count: int = 0
    incident_count: int = 0
    risk_level: str = "LOW"
    safety_score: float = 100.0

class WorkgroupSafetyProfile(BaseModel):
    group_id: str
    group_name: str
    worker_count: int = 0
    average_safety_score: float = 100.0
    common_violations: List[str] = Field(default_factory=list)
    incident_frequency: float = 0.0
    ppe_compliance_rate: float = 100.0
    safety_trend: str = "STABLE"

class SafetyChangeRecord(BaseModel):
    project_id: str
    previous_score: float
    current_score: float
    score_delta: float
    new_findings_count: int
    resolved_findings_count: int
    movement_summary: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SafetyMetric(BaseModel):
    metric_name: str
    metric_value: float
    category: str
    status: str
    description: str
