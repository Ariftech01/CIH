from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class ComponentScoreResult(BaseModel):
    category: str
    score: float
    weight: float = 1.0
    status: str = "NORMAL"
    breakdown: Dict[str, Any] = Field(default_factory=dict)

class RiskScoreResponse(BaseModel):
    id: str
    assessment_id: str
    project_id: str
    category: str
    score: float
    weight: float
    status: str
    breakdown_json: Optional[str] = None
    calculated_at: datetime

    class Config:
        from_attributes = True

class UnifiedRiskOutput(BaseModel):
    overall_score: float
    risk_level: str
    component_scores: Dict[str, ComponentScoreResult]
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
