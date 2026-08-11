from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class RiskAssessmentCreate(BaseModel):
    project_id: str
    assessment_type: str = "FULL"
    version: str = "1.0.0"

class RiskAssessmentResponse(BaseModel):
    id: str
    project_id: str
    assessment_type: str
    overall_risk_score: float
    risk_level: str
    status: str
    version: str
    summary: Optional[str] = None
    evaluated_at: datetime

    class Config:
        from_attributes = True

class ProjectContext(BaseModel):
    project_id: str
    project_name: str
    budget: float = 0.0
    status: str = "PLANNED"
    worker_count: int = 0
    equipment_count: int = 0
    material_count: int = 0
    safety_inspections_count: int = 0
    incidents_count: int = 0
    raw_data: Dict[str, Any] = Field(default_factory=dict)
