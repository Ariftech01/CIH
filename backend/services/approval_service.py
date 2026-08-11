from datetime import datetime
from typing import List, Optional
from backend.database.session import get_db_session
from backend.repositories.approval_repository import ApprovalRepository
from backend.schemas.approval import ApprovalCreate, ApprovalUpdate, ApprovalResponse

class ApprovalService:
    def create_approval_request(self, app_in: ApprovalCreate) -> ApprovalResponse:
        with get_db_session() as session:
            repo = ApprovalRepository(session)
            appr = repo.create(app_in.model_dump())
            return ApprovalResponse.model_validate(appr)

    def process_approval(self, approval_id: str, update_in: ApprovalUpdate) -> ApprovalResponse:
        with get_db_session() as session:
            repo = ApprovalRepository(session)
            data = update_in.model_dump()
            data["approval_time"] = datetime.utcnow()
            appr = repo.update(approval_id, data)
            return ApprovalResponse.model_validate(appr)

    def get_pending_approvals(self, project_id: str = None) -> List[ApprovalResponse]:
        with get_db_session() as session:
            repo = ApprovalRepository(session)
            apps = repo.get_pending(project_id)
            return [ApprovalResponse.model_validate(a) for a in apps]

approval_service = ApprovalService()
