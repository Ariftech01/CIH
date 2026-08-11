from datetime import datetime
from typing import Optional, List
from backend.schemas.common import BaseSchema, AuditSchema

class AIMessageBase(BaseSchema):
    sender: str
    message: str
    tokens: Optional[int] = 0

class AIMessageCreate(AIMessageBase):
    conversation_id: str

class AIMessageResponse(AIMessageBase, AuditSchema):
    conversation_id: str

class AIConversationBase(BaseSchema):
    conversation_title: str = "New Conversation"

class AIConversationCreate(AIConversationBase):
    user_id: Optional[str] = None
    project_id: Optional[str] = None

class AIConversationResponse(AIConversationBase, AuditSchema):
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    started_at: datetime
    last_message_at: datetime

class AIPredictionCreate(BaseSchema):
    project_id: Optional[str] = None
    prediction_type: str
    prediction_result: str
    confidence_score: float = 0.0

class AIPredictionResponse(AuditSchema):
    project_id: Optional[str] = None
    prediction_type: str
    prediction_result: str
    confidence_score: float
    generated_at: datetime
