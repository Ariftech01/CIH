from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Approval(BaseModel):
    __tablename__ = "approvals"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    approval_type: Mapped[str] = mapped_column(String(50), nullable=False) # BUDGET, COST_ESTIMATE, MATERIAL_REQUEST, SAFETY_INSPECTION, REPORT
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", nullable=False) # PENDING, APPROVED, REJECTED, UNDER_REVIEW
    requested_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    approval_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="approvals")
