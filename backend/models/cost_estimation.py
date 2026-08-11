from datetime import datetime
from typing import Optional
from sqlalchemy import String, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class CostEstimation(BaseModel):
    __tablename__ = "cost_estimations"
    __table_args__ = (
        CheckConstraint("estimated_total_cost >= 0", name="check_estimated_total_cost_non_negative"),
    )

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    estimated_material_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_labour_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_equipment_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_total_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    calculated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="cost_estimations")
