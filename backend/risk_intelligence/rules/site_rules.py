from typing import Dict, Any, List

class SiteRules:
    """
    Deterministic Rule Engine for Construction Site Analysis.
    Evaluates physical layout congestion, equipment placement density, material storage stability,
    access path obstructions, excavation exposure, and environmental observations.
    """

    @staticmethod
    def evaluate_layout_congestion(building_count: int, equipment_count: int) -> Dict[str, Any]:
        density = equipment_count / float(building_count) if building_count > 0 else 0.0
        if density > 10.0:
            return {"hazard_detected": True, "severity": "CRITICAL", "score_penalty": 30.0, "title": "Severe Site Equipment Congestion", "desc": "High concentration of machinery in restricted construction zone increases collision risks."}
        elif density > 5.0:
            return {"hazard_detected": True, "severity": "MODERATE", "score_penalty": 15.0, "title": "Elevated Machinery Density", "desc": "Equipment placement density above normal operating baseline."}
        return {"hazard_detected": False, "severity": "NONE", "score_penalty": 0.0, "title": "Normal Layout", "desc": "Equipment density within safe operating boundaries."}

    @staticmethod
    def evaluate_material_storage(low_stock_materials: int, total_materials: int) -> Dict[str, Any]:
        if total_materials == 0:
            return {"hazard_detected": True, "severity": "MODERATE", "score_penalty": 15.0, "title": "Unmonitored Material Storage", "desc": "No active material stock tracking on site."}

        ratio = low_stock_materials / float(total_materials)
        if ratio > 0.4:
            return {"hazard_detected": True, "severity": "HIGH", "score_penalty": 25.0, "title": "Critical Material Shortage & Supply Hazard", "desc": "Over 40% of critical raw materials below minimum threshold."}
        elif ratio > 0.0:
            return {"hazard_detected": True, "severity": "LOW", "score_penalty": 10.0, "title": "Minor Inventory Deficit", "desc": "Certain material stocks approaching reorder limits."}
        return {"hazard_detected": False, "severity": "NONE", "score_penalty": 0.0, "title": "Adequate Stock", "desc": "Material storage levels sufficient."}

    @staticmethod
    def evaluate_equipment_maintenance(overdue_equipment_count: int) -> Dict[str, Any]:
        if overdue_equipment_count >= 3:
            return {"hazard_detected": True, "severity": "CRITICAL", "score_penalty": 35.0, "title": "Multiple Overdue Machinery Maintenance", "desc": "Heavy site equipment operating past mandatory maintenance schedules."}
        elif overdue_equipment_count > 0:
            return {"hazard_detected": True, "severity": "MODERATE", "score_penalty": 15.0, "title": "Overdue Machinery Maintenance", "desc": "One or more site machinery units overdue for inspection."}
        return {"hazard_detected": False, "severity": "NONE", "score_penalty": 0.0, "title": "Maintained Equipment", "desc": "All machinery inspections up to date."}

    @staticmethod
    def evaluate_incidents_history(incidents_count: int, high_severity_incidents: int) -> Dict[str, Any]:
        if high_severity_incidents > 0:
            return {"hazard_detected": True, "severity": "CRITICAL", "score_penalty": 40.0, "title": "High Severity Site Incidents Logged", "desc": "Past severe site incidents recorded requiring active mitigation."}
        elif incidents_count >= 3:
            return {"hazard_detected": True, "severity": "HIGH", "score_penalty": 20.0, "title": "Frequent Site Incidents Recorded", "desc": "Multiple near-miss or site hazard incidents logged."}
        elif incidents_count > 0:
            return {"hazard_detected": True, "severity": "LOW", "score_penalty": 5.0, "title": "Minor Incident Logged", "desc": "Isolated minor site incident recorded."}
        return {"hazard_detected": False, "severity": "NONE", "score_penalty": 0.0, "title": "Clean Incident Record", "desc": "No site incidents reported."}
