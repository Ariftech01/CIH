from typing import List, Optional, Dict, Any
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
    def get_user_conversations(self, user_id: Optional[str] = None) -> List[Any]:
        with get_db_session() as session:
            repo = AIRepository(session)
            convs = repo.get_user_conversations(user_id)
            res = []
            for c in convs:
                msgs = [
                    {"role": m.sender, "content": m.message, "time": m.created_at.strftime("%H:%M") if m.created_at else ""}
                    for m in (c.messages or [])
                ]
                res.append({
                    "id": c.id,
                    "title": c.conversation_title,
                    "created_at": c.started_at.strftime("%b %d, %H:%M") if c.started_at else "",
                    "last_modified": c.last_message_at.strftime("%b %d, %H:%M") if c.last_message_at else "",
                    "pinned": False,
                    "messages": msgs,
                    "active_doc": None
                })
            return res

    def get_conversation_history(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        with get_db_session() as session:
            repo = AIRepository(session)
            c = repo.get_conversation_history(conversation_id)
            if not c:
                return None
            msgs = [
                {"role": m.sender, "content": m.message, "time": m.created_at.strftime("%H:%M") if m.created_at else ""}
                for m in (c.messages or [])
            ]
            return {
                "id": c.id,
                "title": c.conversation_title,
                "created_at": c.started_at.strftime("%b %d, %H:%M") if c.started_at else "",
                "last_modified": c.last_message_at.strftime("%b %d, %H:%M") if c.last_message_at else "",
                "pinned": False,
                "messages": msgs,
                "active_doc": None
            }

    def update_conversation_title(self, conversation_id: str, new_title: str) -> bool:
        with get_db_session() as session:
            repo = AIRepository(session)
            conv = repo.update_conversation_title(conversation_id, new_title)
            return conv is not None

    def delete_conversation(self, conversation_id: str) -> bool:
        with get_db_session() as session:
            repo = AIRepository(session)
            return repo.delete_conversation(conversation_id)

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
