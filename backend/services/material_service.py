from typing import List, Dict, Any
from backend.database.session import get_db_session
from backend.repositories.material_repository import MaterialRepository
from backend.schemas.material import MaterialCreate, MaterialResponse
from backend.utils.exceptions import MaterialNotFound
from backend.validators.input_validators import validate_positive_number

class MaterialService:
    def add_material(self, mat_in: MaterialCreate) -> MaterialResponse:
        qty_req = validate_positive_number(mat_in.quantity_required, "quantity_required")
        unit_cost = validate_positive_number(mat_in.unit_cost, "unit_cost")

        with get_db_session() as session:
            repo = MaterialRepository(session)
            data = mat_in.model_dump()
            data["total_cost"] = qty_req * unit_cost
            mat = repo.create(data)
            return MaterialResponse.model_validate(mat)

    def get_project_materials(self, project_id: str) -> List[MaterialResponse]:
        with get_db_session() as session:
            repo = MaterialRepository(session)
            mats = repo.get_by_project(project_id)
            return [MaterialResponse.model_validate(m) for m in mats]

    def get_inventory_summary(self, project_id: str) -> Dict[str, Any]:
        with get_db_session() as session:
            repo = MaterialRepository(session)
            return repo.get_inventory_summary(project_id)

material_service = MaterialService()
