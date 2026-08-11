from typing import Dict, Any, List

class DelayAnalyzer:
    """
    Analyzes project milestone progress and schedule slippage risks.
    """
    def analyze(self, progress_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not progress_records:
            return {"delay_risk_score": 10.0, "status": "ON_SCHEDULE"}

        latest = progress_records[-1]
        planned = latest.get("planned_completion", 0.0)
        actual = latest.get("actual_completion", 0.0)
        variance = planned - actual

        if variance <= 0:
            score = 0.0
            status = "ON_SCHEDULE"
        elif variance <= 10.0:
            score = 25.0
            status = "MINOR_SLIPPAGE"
        else:
            score = min(variance * 3.5, 100.0)
            status = "MAJOR_SLIPPAGE"

        return {
            "planned_completion": planned,
            "actual_completion": actual,
            "schedule_variance": variance,
            "delay_risk_score": score,
            "status": status
        }
