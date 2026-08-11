from typing import Dict, Any, List

class WorkforceAnalyzer:
    """
    Analyzes workforce allocation, certified personnel coverage, and safety training status.
    """
    def analyze(self, worker_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(worker_data)
        if total == 0:
            return {"workforce_risk": 20.0, "uncertified_count": 0, "status": "NO_WORKERS"}

        active = sum(1 for w in worker_data if w.get("status") == "ACTIVE")
        certified = sum(1 for w in worker_data if w.get("is_certified", True))
        uncertified = total - certified

        risk = (uncertified / float(total)) * 50.0 + (0.0 if active > 0 else 30.0)

        return {
            "total_workers": total,
            "active_workers": active,
            "certified_workers": certified,
            "uncertified_workers": uncertified,
            "workforce_risk_score": min(risk, 100.0),
            "status": "OPTIMAL" if uncertified == 0 else "CERTIFICATION_DEFICIT"
        }
