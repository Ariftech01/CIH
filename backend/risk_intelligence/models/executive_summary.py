from typing import Optional
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class ExecutiveSummary(BaseModel):
    """
    Generated executive narrative summaries persisted per assessment or period.
    """
    __tablename__ = "cri_executive_summaries"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    headline: Mapped[str] = mapped_column(String(255), nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    key_findings_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_type: Mapped[str] = mapped_column(String(30), default="CIH_AI", nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assessment: Mapped["RiskAssessment"] = relationship("RiskAssessment", backref="executive_summaries")
    project: Mapped["Project"] = relationship("Project", backref="cri_executive_summaries")
