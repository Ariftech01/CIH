from typing import Dict, Any
from backend.risk_intelligence.constants import DEFAULT_COMPONENT_WEIGHTS, RiskLevel, CRITICAL_RISK_THRESHOLD, HIGH_RISK_THRESHOLD, MODERATE_RISK_THRESHOLD
from backend.risk_intelligence.utils.helpers import normalize_risk_score, categorize_risk_level

class RiskAggregatorEngine:
    """
    Central Risk Aggregation Engine & Unified Scoring Framework.
    Combines component risk scores deterministically, applies configurable weighting,
    normalizes output to [0.0, 100.0], calculates confidence indicators, and supports incomplete analyses.
    """

    def aggregate(self, component_scores: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        if not component_scores:
            return {
                "overall_risk_score": 0.0,
                "risk_level": RiskLevel.LOW.value,
                "confidence_score": 0.0,
                "components_evaluated": 0
            }

        total_weighted_score = 0.0
        total_weight = 0.0

        for comp_name, comp_data in component_scores.items():
            score = normalize_risk_score(comp_data.get("score", 0.0))
            weight = float(comp_data.get("weight", DEFAULT_COMPONENT_WEIGHTS.get(comp_name, 1.0)))
            total_weighted_score += score * weight
            total_weight += weight

        overall_score = round(total_weighted_score / total_weight, 2) if total_weight > 0 else 0.0
        overall_score = normalize_risk_score(overall_score)
        risk_level = categorize_risk_level(overall_score)

        # Estimate confidence score based on component completeness
        expected_total_components = 5
        evaluated_count = len(component_scores)
        confidence_score = round((evaluated_count / float(expected_total_components)) * 100.0, 1)

        return {
            "overall_risk_score": overall_score,
            "risk_level": risk_level,
            "confidence_score": confidence_score,
            "components_evaluated": evaluated_count
        }

risk_aggregator_engine = RiskAggregatorEngine()
