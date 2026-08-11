from typing import Optional
from sqlalchemy import String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class Room(BaseModel):
    __tablename__ = "rooms"
    __table_args__ = (
        CheckConstraint("length > 0", name="check_room_length_positive"),
        CheckConstraint("width > 0", name="check_room_width_positive"),
        CheckConstraint("height > 0", name="check_room_height_positive"),
        CheckConstraint("area >= 0", name="check_room_area_non_negative"),
    )

    floor_id: Mapped[str] = mapped_column(String(36), ForeignKey("floors.id", ondelete="CASCADE"), nullable=False, index=True)
    room_name: Mapped[str] = mapped_column(String(100), nullable=False)
    room_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    length: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    width: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    height: Mapped[float] = mapped_column(Float, default=3.0, nullable=False)
    area: Mapped[float] = mapped_column(Float, default=16.0, nullable=False)
    perimeter: Mapped[float] = mapped_column(Float, default=16.0, nullable=False)
    volume: Mapped[float] = mapped_column(Float, default=48.0, nullable=False)
    wall_thickness: Mapped[float] = mapped_column(Float, default=0.23, nullable=False)

    # Relationships
    floor: Mapped["Floor"] = relationship("Floor", back_populates="rooms")
