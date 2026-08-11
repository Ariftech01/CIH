from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SiteHazard(BaseModel):
    hazard_id: str
    category: str
    title: str
    severity: str  # MINOR, MODERATE, MAJOR, CRITICAL
    description: str
    location: Optional[str] = None
    business_justification: str
    evidence: Optional[str] = None

class SiteFinding(BaseModel):
    category: str
    title: str
    description: str
    severity: str
    location: Optional[str] = None
    evidence: Optional[str] = None
    suggested_action: str

class SiteMonitoringSession(BaseModel):
    session_id: str
    project_id: str
    assessment_timestamp: datetime = Field(default_factory=datetime.utcnow)
    observed_conditions_count: int = 0
    hazards_detected_count: int = 0
    site_risk_score: float = 0.0
    findings: List[SiteFinding] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SiteState(BaseModel):
    project_id: str
    current_site_risk_score: float = 0.0
    health_status: str = "HEALTHY"
    active_hazards_count: int = 0
    critical_hazards_count: int = 0
    last_session_id: Optional[str] = None
    last_evaluated_at: datetime = Field(default_factory=datetime.utcnow)
