import time
from typing import List, Optional
from backend.database.session import get_db_session
from backend.repositories.project_repository import ProjectRepository
from backend.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.utils.exceptions import ProjectNotFound, DuplicateProjectError
from backend.validators.input_validators import validate_project_code, validate_positive_number

def invalidate_project_caches() -> None:
    """Invalidate project list caches and analytics engine caches on data mutation."""
    try:
        from backend.cache.cache_manager import cache_manager
        cache_manager.invalidate("dashboard_kpis")
    except Exception:
        pass

    try:
        from app import _get_cached_sidebar_projects
        _get_cached_sidebar_projects.clear()
    except Exception:
        pass


class ProjectService:
    def generate_unique_project_code(self, base_code: str) -> str:
        """Generate next available unique project code if base_code is already taken."""
        try:
            base_code = validate_project_code(base_code)
        except Exception:
            base_code = "PRJ-GEN-001"

        with get_db_session() as session:
            repo = ProjectRepository(session)
            if not repo.get_by_code(base_code, include_deleted=True):
                return base_code
            
            import re
            match = re.match(r"^(.*?)-(\d+)$", base_code)
            if match:
                prefix, num_str = match.group(1), match.group(2)
                counter = int(num_str) + 1
                padding = max(3, len(num_str))
            else:
                prefix = base_code
                counter = 1
                padding = 3

            while counter < 10000:
                candidate = f"{prefix}-{str(counter).zfill(padding)}"
                if not repo.get_by_code(candidate, include_deleted=True):
                    return candidate
                counter += 1
            return f"{prefix}-{int(time.time())}"

    def create_project(self, project_in: ProjectCreate) -> ProjectResponse:
        code = validate_project_code(project_in.project_code)
        validate_positive_number(project_in.budget, "budget")

        with get_db_session() as session:
            repo = ProjectRepository(session)
            if repo.get_by_code(code):
                raise DuplicateProjectError(f"Project with code '{code}' already exists.")

            data = project_in.model_dump()
            data["project_code"] = code
            project = repo.create(data)
            invalidate_project_caches()
            return ProjectResponse.model_validate(project)

    def get_project_by_id(self, project_id: str) -> ProjectResponse:
        with get_db_session() as session:
            repo = ProjectRepository(session)
            project = repo.get_by_id(project_id)
            if not project:
                raise ProjectNotFound(project_id)
            return ProjectResponse.model_validate(project)

    def get_project_by_code(self, project_code: str) -> Optional[ProjectResponse]:
        with get_db_session() as session:
            repo = ProjectRepository(session)
            project = repo.get_by_code(project_code)
            if not project:
                return None
            return ProjectResponse.model_validate(project)

    def get_all_projects(self, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
        with get_db_session() as session:
            repo = ProjectRepository(session)
            projects = repo.get_all(skip=skip, limit=limit)
            return [ProjectResponse.model_validate(p) for p in projects]

    def update_project(self, project_id: str, update_in: ProjectUpdate) -> ProjectResponse:
        with get_db_session() as session:
            repo = ProjectRepository(session)
            if not repo.exists(project_id):
                raise ProjectNotFound(project_id)

            data = {k: v for k, v in update_in.model_dump().items() if v is not None}
            updated = repo.update(project_id, data)
            invalidate_project_caches()
            return ProjectResponse.model_validate(updated)

    def archive_project(self, project_id: str) -> ProjectResponse:
        return self.update_project(project_id, ProjectUpdate(status="COMPLETED"))

    def soft_delete_project(self, project_id: str) -> bool:
        with get_db_session() as session:
            repo = ProjectRepository(session)
            if not repo.exists(project_id):
                raise ProjectNotFound(project_id)
            return repo.soft_delete(project_id)

    def search_projects(self, query: str) -> List[ProjectResponse]:
        with get_db_session() as session:
            repo = ProjectRepository(session)
            projects = repo.search_projects(query)
            return [ProjectResponse.model_validate(p) for p in projects]

project_service = ProjectService()
