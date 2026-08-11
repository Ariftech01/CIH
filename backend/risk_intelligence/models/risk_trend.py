from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class RiskTrend(BaseModel):
    """
    Aggregated historical risk trend entity (e.g. daily/weekly/monthly risk metrics).
    """
    __tablename__ = "cri_risk_trends"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    period_type: Mapped[str] = mapped_column(String(20), default="WEEKLY", nullable=False, index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    avg_risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    peak_risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    incident_count: Mapped[int] = mapped_column(default=0, nullable=False)
    trend_direction: Mapped[str] = mapped_column(String(20), default="STABLE", nullable=False)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="cri_risk_trends")
