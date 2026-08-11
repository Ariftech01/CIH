from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class RiskSnapshot(BaseModel):
    """
    Immutable project risk snapshot for historical comparison and analytics.
    """
    __tablename__ = "cri_risk_snapshots"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="SET NULL"), nullable=True, index=True
    )
    snapshot_tag: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    snapshot_data_json: Mapped[str] = mapped_column(Text, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="cri_risk_snapshots")
    assessment: Mapped[Optional["RiskAssessment"]] = relationship("RiskAssessment", backref="cri_risk_snapshots")
