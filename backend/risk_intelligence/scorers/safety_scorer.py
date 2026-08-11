from typing import Dict, Any
from backend.risk_intelligence.schemas.score import ComponentScoreResult
from backend.risk_intelligence.rules.safety_rules import SafetyRules

class SafetyScorer:
    """
    Calculates Safety Risk Score based on PPE compliance rates, hazard observations, and safety inspections.
    """
    def calculate_score(self, context_data: Dict[str, Any]) -> ComponentScoreResult:
        inspections_count = context_data.get("safety_inspections_count", 0)
        incidents_count = context_data.get("incidents_count", 0)
        ppe_compliance = context_data.get("ppe_compliance_rate", 92.0)

        ppe_eval = SafetyRules.evaluate_ppe_compliance(ppe_compliance)
        incident_eval = SafetyRules.evaluate_incident_frequency(incidents_count)

        raw_risk = ppe_eval["score_penalty"] + incident_eval["score_penalty"]
        if inspections_count == 0:
            raw_risk += 25.0  # Audit penalty

        score = min(max(raw_risk, 0.0), 100.0)
        status = "HIGH" if score > 50 else ("MEDIUM" if score > 20 else "LOW")

        return ComponentScoreResult(
            category="Safety",
            score=score,
            weight=1.5,
            status=status,
            breakdown={
                "ppe_compliance_rate": ppe_compliance,
                "safety_inspections_count": inspections_count,
                "incidents_count": incidents_count,
                "ppe_status": ppe_eval["status"],
                "incident_status": incident_eval["status"]
            }
        )
