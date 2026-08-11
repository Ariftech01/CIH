from typing import Optional
from sqlalchemy import String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Worker(BaseModel):
    __tablename__ = "workers"
    __table_args__ = (
        CheckConstraint("daily_wage >= 0", name="check_worker_daily_wage_non_negative"),
    )

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    worker_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    designation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    daily_wage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    attendance: Mapped[Optional[str]] = mapped_column(String(20), default="PRESENT", nullable=True)
    assigned_task: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="ACTIVE", nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="workers")
