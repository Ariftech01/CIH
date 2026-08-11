from typing import List, Optional
from backend.database.session import get_db_session
from backend.repositories.ai_repository import AIRepository
from backend.schemas.ai import (
    AIConversationCreate, AIConversationResponse,
    AIMessageCreate, AIMessageResponse,
    AIPredictionCreate, AIPredictionResponse
)
from backend.schemas.document import DocumentCreate, DocumentResponse

class AIService:
    def create_conversation(self, conv_in: AIConversationCreate) -> AIConversationResponse:
        with get_db_session() as session:
            repo = AIRepository(session)
            conv = repo.create_conversation(
                user_id=conv_in.user_id,
                project_id=conv_in.project_id,
                title=conv_in.conversation_title
            )
            return AIConversationResponse.model_validate(conv)

    def add_message(self, msg_in: AIMessageCreate) -> AIMessageResponse:
        with get_db_session() as session:
            repo = AIRepository(session)
            msg = repo.add_message(
                conversation_id=msg_in.conversation_id,
                sender=msg_in.sender,
                message=msg_in.message,
                tokens=msg_in.tokens or 0
            )
            return AIMessageResponse.model_validate(msg)

    def save_prediction(self, pred_in: AIPredictionCreate) -> AIPredictionResponse:
        with get_db_session() as session:
            repo = AIRepository(session)
            pred = repo.save_prediction(
                project_id=pred_in.project_id,
                prediction_type=pred_in.prediction_type,
                result=pred_in.prediction_result,
                confidence=pred_in.confidence_score
            )
            return AIPredictionResponse.model_validate(pred)

    def save_document(self, doc_in: DocumentCreate) -> DocumentResponse:
        with get_db_session() as session:
            repo = AIRepository(session)
            doc = repo.save_document_metadata(
                file_name=doc_in.file_name,
                file_type=doc_in.file_type,
                file_size=doc_in.file_size,
                storage_path=doc_in.storage_path,
                project_id=doc_in.project_id,
                conversation_id=doc_in.conversation_id
            )
            return DocumentResponse.model_validate(doc)

ai_service = AIService()
