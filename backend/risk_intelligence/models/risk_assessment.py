from typing import Optional, List
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class RiskAssessment(BaseModel):
    """
    Parent entity representing one complete risk analysis execution run.
    """
    __tablename__ = "cri_risk_assessments"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_type: Mapped[str] = mapped_column(String(50), default="FULL", nullable=False)
    overall_risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(30), default="LOW", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), default="COMPLETED", nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0", nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="cri_risk_assessments")
    risk_scores: Mapped[List["ProjectRiskScore"]] = relationship(
        "ProjectRiskScore", back_populates="assessment", cascade="all, delete-orphan"
    )
    recommendations: Mapped[List["RiskRecommendation"]] = relationship(
        "RiskRecommendation", back_populates="assessment", cascade="all, delete-orphan"
    )
    safety_assessments: Mapped[List["SafetyAssessment"]] = relationship(
        "SafetyAssessment", back_populates="assessment", cascade="all, delete-orphan"
    )
    compliance_assessments: Mapped[List["ComplianceAssessment"]] = relationship(
        "ComplianceAssessment", back_populates="assessment", cascade="all, delete-orphan"
    )
    insurance_assessments: Mapped[List["InsuranceAssessment"]] = relationship(
        "InsuranceAssessment", back_populates="assessment", cascade="all, delete-orphan"
    )
    agent_executions: Mapped[List["AgentExecution"]] = relationship(
        "AgentExecution", back_populates="assessment", cascade="all, delete-orphan"
    )
