from typing import Optional, List
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from backend.models.project import Project
from backend.repositories.base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: Session):
        super().__init__(Project, session)

    def get_by_code(self, project_code: str, include_deleted: bool = False) -> Optional[Project]:
        stmt = select(Project).where(Project.project_code == project_code)
        if not include_deleted:
            stmt = stmt.where(Project.is_deleted == False)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_active_projects(self) -> List[Project]:
        stmt = select(Project).where(
            Project.is_deleted == False,
            Project.status.in_(["PLANNED", "IN_PROGRESS"])
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_completed_projects(self) -> List[Project]:
        stmt = select(Project).where(Project.is_deleted == False, Project.status == "COMPLETED")
        return list(self.session.execute(stmt).scalars().all())

    def search_projects(self, query: str) -> List[Project]:
        stmt = select(Project).where(
            Project.is_deleted == False,
            or_(
                Project.project_name.ilike(f"%{query}%"),
                Project.project_code.ilike(f"%{query}%"),
                Project.client_name.ilike(f"%{query}%")
            )
        )
        return list(self.session.execute(stmt).scalars().all())
