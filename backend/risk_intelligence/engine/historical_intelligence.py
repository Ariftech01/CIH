from typing import List, Dict, Any, Optional

class HistoricalIntelligenceEngine:
    """
    Historical Intelligence Framework.
    Analyzes historical risk assessments, calculates trends (Improving, Stable, Declining),
    detects pattern shifts, and performs baseline comparisons across project milestones.
    """

    def analyze_trends(self, historical_assessments: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not historical_assessments:
            return {
                "trend_direction": "STABLE",
                "delta_score": 0.0,
                "assessment_count": 0,
                "historical_pattern": "INSUFFICIENT_DATA"
            }

        scores = [a.get("overall_risk_score", 0.0) for a in historical_assessments]
        count = len(scores)

        if count < 2:
            return {
                "trend_direction": "STABLE",
                "delta_score": 0.0,
                "assessment_count": count,
                "historical_pattern": "BASELINE_ESTABLISHED"
            }

        first_score = scores[-1]  # Oldest
        latest_score = scores[0]  # Newest
        delta = latest_score - first_score

        if delta < -5.0:
            direction = "IMPROVING"  # Lower risk score is better
        elif delta > 5.0:
            direction = "DECLINING"  # Higher risk score is worse
        else:
            direction = "STABLE"

        return {
            "trend_direction": direction,
            "delta_score": round(delta, 2),
            "assessment_count": count,
            "first_score": first_score,
            "latest_score": latest_score,
            "historical_pattern": f"RISK_{direction}"
        }

historical_intelligence_engine = HistoricalIntelligenceEngine()
