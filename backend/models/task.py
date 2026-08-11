from datetime import date
from typing import Optional
from sqlalchemy import String, Text, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Task(BaseModel):
    __tablename__ = "tasks"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    building_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("buildings.id", ondelete="SET NULL"), nullable=True)
    floor_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("floors.id", ondelete="SET NULL"), nullable=True)

    task_name: Mapped[str] = mapped_column(String(150), nullable=False)
    task_category: Mapped[Optional[str]] = mapped_column(String(50), default="General Construction", nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", nullable=False) # PENDING, IN_PROGRESS, BLOCKED, COMPLETED, CANCELLED
    priority: Mapped[str] = mapped_column(String(20), default="MEDIUM", nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    completion_percentage: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    parent_task_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="tasks")
