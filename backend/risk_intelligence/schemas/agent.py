from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class AgentResult(BaseModel):
    agent_name: str
    status: str = "SUCCESS"
    score: float = 0.0
    weight: float = 1.0
    duration_ms: float = 0.0
    summary: str = ""
    findings: Dict[str, Any] = Field(default_factory=dict)
    recommendations: list = Field(default_factory=list)
    error_message: Optional[str] = None

class AgentExecutionResponse(BaseModel):
    id: str
    assessment_id: str
    agent_name: str
    execution_status: str
    duration_ms: float
    output_summary: Optional[str] = None
    error_message: Optional[str] = None
    executed_at: datetime

    class Config:
        from_attributes = True
