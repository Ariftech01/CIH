from typing import Dict, Any, List
from backend.risk_intelligence.exceptions import InvalidProjectContextError

class DataQualityValidator:
    """
    Sanitizes and checks operational data quality prior to risk engine analysis.
    """
    @staticmethod
    def sanitize_context(context_data: Dict[str, Any]) -> Dict[str, Any]:
        if not context_data:
            raise InvalidProjectContextError("Project context data cannot be empty.")

        sanitized = dict(context_data)
        sanitized["budget"] = max(float(sanitized.get("budget", 0.0)), 0.0)
        sanitized["worker_count"] = max(int(sanitized.get("worker_count", 0)), 0)
        sanitized["equipment_count"] = max(int(sanitized.get("equipment_count", 0)), 0)
        sanitized["incidents_count"] = max(int(sanitized.get("incidents_count", 0)), 0)
        return sanitized
