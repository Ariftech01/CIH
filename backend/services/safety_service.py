from typing import List
from backend.database.session import get_db_session
from backend.repositories.safety_repository import SafetyRepository
from backend.schemas.safety import SafetyInspectionCreate, SafetyInspectionResponse

class SafetyService:
    def record_inspection(self, insp_in: SafetyInspectionCreate) -> SafetyInspectionResponse:
        with get_db_session() as session:
            repo = SafetyRepository(session)
            insp = repo.create(insp_in.model_dump())
            return SafetyInspectionResponse.model_validate(insp)

    def get_project_inspections(self, project_id: str) -> List[SafetyInspectionResponse]:
        with get_db_session() as session:
            repo = SafetyRepository(session)
            insps = repo.get_by_project(project_id)
            return [SafetyInspectionResponse.model_validate(i) for i in insps]

safety_service = SafetyService()
