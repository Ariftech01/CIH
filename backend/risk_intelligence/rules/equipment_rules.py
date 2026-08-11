from typing import Dict, Any

class EquipmentRules:
    """
    Equipment operational status and maintenance risk evaluation rules.
    """
    @staticmethod
    def evaluate_equipment_status(maintenance_overdue_count: int, total_equipment: int) -> Dict[str, Any]:
        if total_equipment == 0:
            return {"status": "NO_EQUIPMENT", "risk_score": 0.0}

        ratio = maintenance_overdue_count / float(total_equipment)
        if ratio == 0:
            return {"status": "HEALTHY", "risk_score": 5.0}
        elif ratio <= 0.2:
            return {"status": "MODERATE_RISK", "risk_score": 25.0}
        else:
            return {"status": "HIGH_RISK", "risk_score": 60.0}
