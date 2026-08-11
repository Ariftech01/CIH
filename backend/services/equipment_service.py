from typing import List, Dict, Any
from backend.database.session import get_db_session
from backend.repositories.equipment_repository import EquipmentRepository
from backend.schemas.equipment import EquipmentCreate, EquipmentResponse

class EquipmentService:
    def add_equipment(self, eq_in: EquipmentCreate) -> EquipmentResponse:
        with get_db_session() as session:
            repo = EquipmentRepository(session)
            eq = repo.create(eq_in.model_dump())
            return EquipmentResponse.model_validate(eq)

    def get_project_equipment(self, project_id: str) -> List[EquipmentResponse]:
        with get_db_session() as session:
            repo = EquipmentRepository(session)
            eqs = repo.get_by_project(project_id)
            return [EquipmentResponse.model_validate(e) for e in eqs]

    def get_equipment_summary(self, project_id: str) -> Dict[str, Any]:
        with get_db_session() as session:
            repo = EquipmentRepository(session)
            return repo.get_equipment_summary(project_id)

equipment_service = EquipmentService()
