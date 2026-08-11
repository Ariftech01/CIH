from typing import Dict, Any, List

class IncidentAnalyzer:
    """
    Analyzes site incident history, severe injuries, property damage, and near-miss frequency.
    """
    def analyze(self, incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(incidents)
        if total == 0:
            return {"incident_risk_score": 0.0, "high_severity_count": 0, "status": "ZERO_INCIDENTS"}

        high_sev = sum(1 for i in incidents if i.get("severity") in ["HIGH", "CRITICAL"])
        impact_sum = sum(i.get("financial_impact", 0.0) for i in incidents)

        score = min(total * 15.0 + high_sev * 25.0, 100.0)

        return {
            "total_incidents": total,
            "high_severity_count": high_sev,
            "total_financial_impact": impact_sum,
            "incident_risk_score": score,
            "status": "CRITICAL_INCIDENTS" if high_sev > 0 else "ELEVATED_INCIDENTS"
        }
