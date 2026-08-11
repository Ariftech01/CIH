from typing import Dict, Any
from backend.risk_intelligence.schemas.score import ComponentScoreResult

class SiteRiskScorer:
    """
    Calculates deterministic Site Risk Score based on environmental, physical, and operational parameters.
    """
    def calculate_score(self, context_data: Dict[str, Any]) -> ComponentScoreResult:
        building_count = context_data.get("building_count", 1)
        equipment_count = context_data.get("equipment_count", 0)
        material_count = context_data.get("material_count", 0)

        # Baseline calculation
        base_score = 10.0 + (building_count * 2.0)
        if equipment_count > 10:
            base_score += 15.0
        if material_count == 0:
            base_score += 20.0  # Supply risk

        score = min(max(base_score, 0.0), 100.0)
        status = "CRITICAL" if score > 70 else ("ELEVATED" if score > 40 else "NORMAL")

        return ComponentScoreResult(
            category="Site Risk",
            score=score,
            weight=1.2,
            status=status,
            breakdown={
                "building_count": building_count,
                "equipment_count": equipment_count,
                "material_count": material_count,
                "raw_site_score": score
            }
        )
