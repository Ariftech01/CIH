from typing import Optional
from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class NotificationLog(BaseModel):
    """
    Log entity for risk alerts and notifications issued by CRI workflows.
    """
    __tablename__ = "cri_notification_logs"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessment_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("cri_risk_assessments.id", ondelete="SET NULL"), nullable=True, index=True
    )
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    recipient: Mapped[str] = mapped_column(String(100), nullable=False)
    channel: Mapped[str] = mapped_column(String(30), default="DASHBOARD", nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_delivered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="cri_notification_logs")
    assessment: Mapped[Optional["RiskAssessment"]] = relationship("RiskAssessment", backref="cri_notification_logs")
