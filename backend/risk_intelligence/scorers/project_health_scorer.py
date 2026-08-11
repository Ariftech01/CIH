from typing import Dict
from backend.risk_intelligence.schemas.score import ComponentScoreResult, UnifiedRiskOutput

class ProjectHealthScorer:
    """
    Combines weighted component risk scores into an Overall Project Risk Score & Health Index.
    """
    def calculate_overall_risk(self, component_scores: Dict[str, ComponentScoreResult]) -> UnifiedRiskOutput:
        total_weighted_score = 0.0
        total_weight = 0.0

        for comp in component_scores.values():
            total_weighted_score += comp.score * comp.weight
            total_weight += comp.weight

        overall_score = (total_weighted_score / total_weight) if total_weight > 0 else 0.0
        overall_score = min(max(round(overall_score, 2), 0.0), 100.0)

        if overall_score >= 70.0:
            level = "CRITICAL"
        elif overall_score >= 40.0:
            level = "HIGH"
        elif overall_score >= 20.0:
            level = "MODERATE"
        else:
            level = "LOW"

        return UnifiedRiskOutput(
            overall_score=overall_score,
            risk_level=level,
            component_scores=component_scores
        )
