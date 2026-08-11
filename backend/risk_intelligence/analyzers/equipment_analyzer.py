from typing import Dict, Any, List

class EquipmentAnalyzer:
    """
    Analyzes equipment operational availability, maintenance schedules, and breakdown risks.
    """
    def analyze(self, equipment_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(equipment_data)
        if total == 0:
            return {"equipment_risk": 0.0, "maintenance_overdue": 0, "status": "NO_EQUIPMENT_DATA"}

        overdue = sum(1 for e in equipment_data if e.get("status") == "MAINTENANCE" or e.get("is_overdue"))
        ratio = overdue / float(total)

        return {
            "total_equipment": total,
            "maintenance_overdue": overdue,
            "overdue_ratio": ratio,
            "equipment_risk_score": min(ratio * 100.0, 100.0),
            "status": "ATTENTION_REQUIRED" if overdue > 0 else "HEALTHY"
        }
