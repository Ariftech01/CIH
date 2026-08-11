from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class ComplianceAssessment(BaseModel):
    """
    Regulatory and code compliance validation entity.
    """
    __tablename__ = "cri_compliance_assessments"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    regulation_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    compliance_status: Mapped[str] = mapped_column(String(30), default="COMPLIANT", nullable=False, index=True)
    violations_count: Mapped[int] = mapped_column(default=0, nullable=False)
    compliance_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    corrective_actions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment: Mapped["RiskAssessment"] = relationship("RiskAssessment", back_populates="compliance_assessments")
    project: Mapped["Project"] = relationship("Project", backref="cri_compliance_assessments")
