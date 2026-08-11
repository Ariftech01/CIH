from typing import Dict, Any
from backend.risk_intelligence.schemas.score import ComponentScoreResult

class InsuranceScorer:
    """
    Calculates Insurance Exposure Score based on overall project budget, active incidents, and safety history.
    """
    def calculate_score(self, context_data: Dict[str, Any]) -> ComponentScoreResult:
        budget = context_data.get("budget", 0.0)
        incidents_count = context_data.get("incidents_count", 0)

        exposure = incidents_count * 15.0
        if budget > 1_000_000:
            exposure += 10.0

        score = min(max(exposure, 0.0), 100.0)
        status = "HIGH_EXPOSURE" if score > 50 else "ACCEPTABLE"

        return ComponentScoreResult(
            category="Insurance Exposure",
            score=score,
            weight=1.0,
            status=status,
            breakdown={
                "project_budget": budget,
                "incidents_count": incidents_count,
                "estimated_exposure_score": score
            }
        )
