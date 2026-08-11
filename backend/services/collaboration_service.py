from typing import List, Optional
from sqlalchemy import select
from backend.database.session import get_db_session
from backend.models.project_member import ProjectMember
from backend.repositories.base_repository import BaseRepository
from backend.schemas.collaboration import ProjectMemberCreate, ProjectMemberResponse

class CollaborationService:
    def add_member(self, member_in: ProjectMemberCreate) -> ProjectMemberResponse:
        with get_db_session() as session:
            repo = BaseRepository(ProjectMember, session)
            pm = repo.create(member_in.model_dump())
            return ProjectMemberResponse.model_validate(pm)

    def get_project_members(self, project_id: str) -> List[ProjectMemberResponse]:
        with get_db_session() as session:
            repo = BaseRepository(ProjectMember, session)
            members = repo.filter(project_id=project_id)
            return [ProjectMemberResponse.model_validate(m) for m in members]

collaboration_service = CollaborationService()
