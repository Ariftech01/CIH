from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.orm import Session, selectinload
from backend.models.ai_conversation import AIConversation
from backend.models.ai_message import AIMessage
from backend.models.document import Document
from backend.models.ai_prediction import AIPrediction
from backend.repositories.base_repository import BaseRepository

class AIRepository:
    def __init__(self, session: Session):
        self.session = session
        self.conversation_repo = BaseRepository(AIConversation, session)
        self.message_repo = BaseRepository(AIMessage, session)
        self.document_repo = BaseRepository(Document, session)
        self.prediction_repo = BaseRepository(AIPrediction, session)

    def create_conversation(self, user_id: str = None, project_id: str = None, title: str = "New Conversation") -> AIConversation:
        return self.conversation_repo.create({
            "user_id": user_id,
            "project_id": project_id,
            "conversation_title": title,
            "started_at": datetime.utcnow(),
            "last_message_at": datetime.utcnow()
        })

    def get_conversation_history(self, conversation_id: str) -> Optional[AIConversation]:
        stmt = (
            select(AIConversation)
            .where(AIConversation.id == conversation_id, AIConversation.is_deleted == False)
            .options(selectinload(AIConversation.messages))
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_user_conversations(self, user_id: str) -> List[AIConversation]:
        stmt = (
            select(AIConversation)
            .where(AIConversation.user_id == user_id, AIConversation.is_deleted == False)
            .order_by(desc(AIConversation.last_message_at))
        )
        return list(self.session.execute(stmt).scalars().all())

    def add_message(self, conversation_id: str, sender: str, message: str, tokens: int = 0) -> AIMessage:
        msg = self.message_repo.create({
            "conversation_id": conversation_id,
            "sender": sender,
            "message": message,
            "tokens": tokens
        })
        conv = self.conversation_repo.get_by_id(conversation_id)
        if conv:
            conv.last_message_at = datetime.utcnow()
            self.session.flush()
        return msg

    def save_prediction(self, project_id: str, prediction_type: str, result: str, confidence: float) -> AIPrediction:
        return self.prediction_repo.create({
            "project_id": project_id,
            "prediction_type": prediction_type,
            "prediction_result": result,
            "confidence_score": confidence,
            "generated_at": datetime.utcnow()
        })

    def save_document_metadata(self, file_name: str, file_type: str, file_size: int, storage_path: str, project_id: str = None, conversation_id: str = None) -> Document:
        return self.document_repo.create({
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_size,
            "storage_path": storage_path,
            "project_id": project_id,
            "conversation_id": conversation_id,
            "uploaded_at": datetime.utcnow()
        })
