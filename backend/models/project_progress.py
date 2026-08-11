from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class ProjectProgress(BaseModel):
    __tablename__ = "project_progress"
    __table_args__ = (
        CheckConstraint("completion_percentage >= 0 AND completion_percentage <= 100", name="check_completion_percentage_range"),
    )

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    planned_progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    actual_progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    delay_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="progress_records")
