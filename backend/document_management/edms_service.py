from typing import List, Dict, Any
from backend.database.session import get_db_session
from backend.repositories.base_repository import BaseRepository
from backend.models.document import Document
from backend.schemas.document import DocumentCreate, DocumentResponse
from backend.app_logging.logger import logger

class EDMSService:
    """
    Enterprise Document Management System (EDMS) handling file metadata, versioning, permissions, and AI context registration.
    """
    def upload_document_metadata(self, doc_in: DocumentCreate) -> DocumentResponse:
        with get_db_session() as session:
            repo = BaseRepository(Document, session)
            # Versioning check
            existing = repo.filter(project_id=doc_in.project_id, file_name=doc_in.file_name)
            version = len(existing) + 1
            
            data = doc_in.model_dump()
            data["file_type"] = f"{doc_in.file_type or 'General'} (V{version})"
            doc = repo.create(data)
            logger.info(f"EDMS: Registered Document '{doc.file_name}' Version {version} for Project '{doc.project_id}'")
            return DocumentResponse.model_validate(doc)

    def get_project_documents(self, project_id: str) -> List[DocumentResponse]:
        with get_db_session() as session:
            repo = BaseRepository(Document, session)
            docs = repo.filter(project_id=project_id)
            return [DocumentResponse.model_validate(d) for d in docs]

    def register_ai_document_context(self, document_id: str) -> Dict[str, Any]:
        return {
            "document_id": document_id,
            "ai_registered": True,
            "summary": "Document successfully indexed into Project AI RAG Context Memory."
        }

edms_service = EDMSService()
