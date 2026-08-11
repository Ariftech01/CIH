from typing import List, Optional
from backend.database.session import get_db_session
from backend.repositories.cost_repository import CostEstimationRepository
from backend.schemas.cost_estimation import CostEstimationCreate, CostEstimationResponse
from backend.validators.input_validators import validate_positive_number

class CostService:
    def create_estimate(self, estimate_in: CostEstimationCreate) -> CostEstimationResponse:
        mat_cost = validate_positive_number(estimate_in.estimated_material_cost, "estimated_material_cost")
        lab_cost = validate_positive_number(estimate_in.estimated_labour_cost, "estimated_labour_cost")
        eq_cost = validate_positive_number(estimate_in.estimated_equipment_cost, "estimated_equipment_cost")

        total = mat_cost + lab_cost + eq_cost

        with get_db_session() as session:
            repo = CostEstimationRepository(session)
            data = estimate_in.model_dump()
            data["estimated_total_cost"] = total
            est = repo.create(data)
            return CostEstimationResponse.model_validate(est)

    def get_latest_estimate(self, project_id: str) -> Optional[CostEstimationResponse]:
        with get_db_session() as session:
            repo = CostEstimationRepository(session)
            est = repo.get_latest_by_project(project_id)
            return CostEstimationResponse.model_validate(est) if est else None

cost_service = CostService()
