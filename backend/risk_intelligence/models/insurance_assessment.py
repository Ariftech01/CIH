from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class InsuranceAssessment(BaseModel):
    """
    Insurance exposure, financial risk liability, and claim readiness assessment entity.
    """
    __tablename__ = "cri_insurance_assessments"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    insurance_category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    estimated_exposure: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    exposure_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    claim_readiness_status: Mapped[str] = mapped_column(String(30), default="READY", nullable=False)
    policy_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment: Mapped["RiskAssessment"] = relationship("RiskAssessment", back_populates="insurance_assessments")
    project: Mapped["Project"] = relationship("Project", backref="cri_insurance_assessments")
