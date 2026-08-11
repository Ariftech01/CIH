from typing import Optional
from sqlalchemy import String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class ProjectRiskScore(BaseModel):
    """
    Component risk score entity for tracking domain-specific scores
    (e.g., Site Risk, Safety, Compliance, Insurance, Delay, Material, Equipment).
    """
    __tablename__ = "cri_project_risk_scores"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="NORMAL", nullable=False)
    breakdown_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment: Mapped["RiskAssessment"] = relationship("RiskAssessment", back_populates="risk_scores")
    project: Mapped["Project"] = relationship("Project", backref="cri_project_risk_scores")
