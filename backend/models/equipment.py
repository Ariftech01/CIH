from datetime import date
from typing import Optional
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Equipment(BaseModel):
    __tablename__ = "equipment"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    equipment_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="OPERATIONAL", nullable=False)
    availability: Mapped[Optional[str]] = mapped_column(String(20), default="AVAILABLE", nullable=True)
    maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    operator: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="equipment")
