from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.models.base import BaseModel

class SystemSettings(BaseModel):
    __tablename__ = "system_settings"

    setting_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    setting_value: Mapped[str] = mapped_column(Text, nullable=False)
