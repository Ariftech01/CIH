from typing import Optional, List
from sqlalchemy import String, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Floor(BaseModel):
    __tablename__ = "floors"
    __table_args__ = (
        CheckConstraint("floor_height > 0", name="check_floor_height_positive"),
        CheckConstraint("area >= 0", name="check_floor_area_non_negative"),
    )

    building_id: Mapped[str] = mapped_column(String(36), ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False, index=True)
    floor_number: Mapped[int] = mapped_column(Integer, nullable=False)
    floor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    floor_height: Mapped[float] = mapped_column(Float, default=3.0, nullable=False)
    area: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relationships
    building: Mapped["Building"] = relationship("Building", back_populates="floors")
    rooms: Mapped[List["Room"]] = relationship("Room", back_populates="floor", cascade="all, delete-orphan")
