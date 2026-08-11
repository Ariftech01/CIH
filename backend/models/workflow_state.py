from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class WorkflowState(BaseModel):
    __tablename__ = "workflow_states"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    current_stage: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False) # DRAFT, PLANNING, DESIGN, ESTIMATION, EXECUTION, MONITORING, COMPLETED, ARCHIVED
    current_status: Mapped[str] = mapped_column(String(50), default="Project Created", nullable=False)
    building_designed: Mapped[bool] = mapped_column(default=False, nullable=False)
    cost_estimated: Mapped[bool] = mapped_column(default=False, nullable=False)
    materials_prepared: Mapped[bool] = mapped_column(default=False, nullable=False)
    workers_assigned: Mapped[bool] = mapped_column(default=False, nullable=False)
    equipment_allocated: Mapped[bool] = mapped_column(default=False, nullable=False)
    safety_inspected: Mapped[bool] = mapped_column(default=False, nullable=False)
    progress_updated: Mapped[bool] = mapped_column(default=False, nullable=False)
    reports_generated: Mapped[bool] = mapped_column(default=False, nullable=False)
    ai_reviewed: Mapped[bool] = mapped_column(default=False, nullable=False)
    predictions_generated: Mapped[bool] = mapped_column(default=False, nullable=False)
    last_transition_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="workflow_state")

class WorkflowHistory(BaseModel):
    __tablename__ = "workflow_histories"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    from_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    to_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    performed_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
