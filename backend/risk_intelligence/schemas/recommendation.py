from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RecommendationCreate(BaseModel):
    assessment_id: str
    project_id: str
    category: str
    priority: str = "MEDIUM"
    title: str
    description: str
    suggested_action: str
    supporting_evidence: Optional[str] = None
    is_ai_generated: bool = False

class RecommendationResponse(BaseModel):
    id: str
    assessment_id: str
    project_id: str
    category: str
    priority: str
    title: str
    description: str
    suggested_action: str
    resolution_status: str
    supporting_evidence: Optional[str] = None
    is_ai_generated: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
