from typing import Optional, List
from sqlalchemy import String, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Building(BaseModel):
    __tablename__ = "buildings"
    __table_args__ = (
        CheckConstraint("total_area >= 0", name="check_building_total_area_non_negative"),
    )

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    building_name: Mapped[str] = mapped_column(String(100), nullable=False)
    building_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    number_of_floors: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_area: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    units: Mapped[Optional[str]] = mapped_column(String(20), default="sqm", nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="buildings")
    floors: Mapped[List["Floor"]] = relationship("Floor", back_populates="building", cascade="all, delete-orphan")
