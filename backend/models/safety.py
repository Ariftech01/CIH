from datetime import date
from typing import Optional
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class SafetyInspection(BaseModel):
    __tablename__ = "safety_inspections"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    inspection_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    risk_level: Mapped[str] = mapped_column(String(20), default="LOW", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    corrective_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="OPEN", nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="safety_inspections")
