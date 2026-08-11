import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class BaseModel(Base):
    """
    Abstract Base Model for all CIH enterprise database entities.
    Provides standard UUID primary keys, audit fields, and soft deletion flags.
    """
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=generate_uuid, 
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    created_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
