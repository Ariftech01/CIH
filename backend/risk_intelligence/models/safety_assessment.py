from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class SafetyAssessment(BaseModel):
    """
    Worker safety, PPE compliance, and site hazard assessment entity.
    """
    __tablename__ = "cri_safety_assessments"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    worker_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("workers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    ppe_compliance_rate: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    unsafe_behaviors_count: Mapped[int] = mapped_column(default=0, nullable=False)
    hazard_level: Mapped[str] = mapped_column(String(30), default="LOW", nullable=False)
    safety_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    findings_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    assessed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment: Mapped["RiskAssessment"] = relationship("RiskAssessment", back_populates="safety_assessments")
    project: Mapped["Project"] = relationship("Project", backref="cri_safety_assessments")
    worker: Mapped[Optional["Worker"]] = relationship("Worker", backref="cri_safety_assessments")
