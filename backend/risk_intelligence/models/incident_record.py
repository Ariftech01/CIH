from typing import Optional
from sqlalchemy import String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from backend.models.base import BaseModel

class IncidentRecord(BaseModel):
    """
    Detailed incident record for safety hazards, equipment failures, near-misses, and site injuries.
    """
    __tablename__ = "cri_incident_records"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    worker_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("workers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    equipment_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True, index=True
    )
    incident_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(20), default="MEDIUM", nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    incident_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), default="OPEN", nullable=False)
    financial_impact: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    corrective_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attachment_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="cri_incident_records")
    worker: Mapped[Optional["Worker"]] = relationship("Worker", backref="cri_incident_records")
    equipment: Mapped[Optional["Equipment"]] = relationship("Equipment", backref="cri_incident_records")
