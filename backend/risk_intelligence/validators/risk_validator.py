from typing import Dict, Any, List

class RiskValidator:
    """
    Subsystem input and data quality validation routines.
    """
    @staticmethod
    def validate_project_context(context_data: Dict[str, Any]) -> List[str]:
        warnings = []
        if not context_data.get("project_id"):
            raise ValueError("project_id is required for Risk Intelligence Analysis.")

        if "worker_count" not in context_data or context_data["worker_count"] == 0:
            warnings.append("No active workers recorded for project context.")

        if "equipment_count" not in context_data or context_data["equipment_count"] == 0:
            warnings.append("No equipment assets linked to project context.")

        return warnings
