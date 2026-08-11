from typing import Optional
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class AIMessage(BaseModel):
    __tablename__ = "ai_messages"

    conversation_id: Mapped[str] = mapped_column(String(36), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sender: Mapped[str] = mapped_column(String(20), nullable=False) # 'user' or 'assistant'
    message: Mapped[str] = mapped_column(Text, nullable=False)
    tokens: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)

    # Relationships
    conversation: Mapped["AIConversation"] = relationship("AIConversation", back_populates="messages")
