from typing import Optional
from sqlalchemy import String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Material(BaseModel):
    __tablename__ = "materials"
    __table_args__ = (
        CheckConstraint("quantity_required >= 0", name="check_material_qty_req_non_negative"),
        CheckConstraint("quantity_available >= 0", name="check_material_qty_avail_non_negative"),
        CheckConstraint("unit_cost >= 0", name="check_material_unit_cost_non_negative"),
    )

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    material_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    unit: Mapped[str] = mapped_column(String(20), default="pcs", nullable=False)
    quantity_required: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quantity_available: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    supplier: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    unit_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="materials")
