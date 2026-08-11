from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class AgentExecution(BaseModel):
    """
    Execution trace entity for auditing individual Risk Agent runs.
    """
    __tablename__ = "cri_agent_executions"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    execution_status: Mapped[str] = mapped_column(String(30), default="SUCCESS", nullable=False)
    duration_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    output_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    assessment: Mapped["RiskAssessment"] = relationship("RiskAssessment", back_populates="agent_executions")
