from typing import Any, Dict
from backend.risk_intelligence.exceptions import InvalidProjectContextError

class EntityValidator:
    """
    Validates required identifier presence, status values, non-null constraints, and entity integrity.
    """
    @staticmethod
    def validate_assessment_creation(project_id: str, assessment_type: str) -> None:
        if not project_id or not isinstance(project_id, str):
            raise InvalidProjectContextError("project_id must be a non-empty string.")

        valid_types = ["FULL", "QUICK", "SCHEDULED", "SAFETY_ONLY", "SITE_ONLY"]
        if assessment_type not in valid_types:
            raise InvalidProjectContextError(f"Invalid assessment_type '{assessment_type}'. Must be one of {valid_types}.")

    @staticmethod
    def validate_incident_creation(project_id: str, title: str, incident_type: str) -> None:
        if not project_id:
            raise InvalidProjectContextError("Incident must be associated with a valid project_id.")

        if not title or len(title.strip()) < 3:
            raise InvalidProjectContextError("Incident title must be at least 3 characters long.")
