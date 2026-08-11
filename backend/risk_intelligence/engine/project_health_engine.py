from typing import Dict, Any

class ProjectHealthEngine:
    """
    Project Health Engine.
    Evaluates overall operational condition and health classification
    (EXCELLENT, GOOD, STABLE, WARNING, CRITICAL) based on unified risk scores and trends.
    """

    def evaluate_health(self, overall_risk_score: float, trend_direction: str = "STABLE") -> Dict[str, Any]:
        score = max(min(overall_risk_score, 100.0), 0.0)

        # Invert score to get Health Index (100 = Best Health, 0 = Worst Health)
        health_index = round(100.0 - score, 1)

        if health_index >= 85.0:
            classification = "EXCELLENT"
            status_desc = "Project operating under optimal safety, site, and compliance parameters."
        elif health_index >= 70.0:
            classification = "GOOD"
            status_desc = "Project condition healthy with minor isolated operational risks."
        elif health_index >= 50.0:
            classification = "STABLE"
            status_desc = "Project condition stable; moderate risk controls active."
        elif health_index >= 30.0:
            classification = "WARNING"
            status_desc = "Elevated project risks detected. Attention required for safety/compliance."
        else:
            classification = "CRITICAL"
            status_desc = "Critical risk levels recorded! Immediate management intervention required."

        return {
            "health_index": health_index,
            "classification": classification,
            "status": classification,
            "status_description": status_desc,
            "trend_direction": trend_direction
        }

    def calculate_project_health(self, overall_risk_score: float = 25.0, component_scores: Dict[str, Any] = None, schedule_delay_days: int = 0, cost_overrun_pct: float = 0.0) -> Dict[str, Any]:
        """Calculate project health based on risk scores, delays, and cost metrics."""
        adjusted_risk = overall_risk_score + (schedule_delay_days * 1.5) + (cost_overrun_pct * 1.2)
        return self.evaluate_health(adjusted_risk)


project_health_engine = ProjectHealthEngine()
