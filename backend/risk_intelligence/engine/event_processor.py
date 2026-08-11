from typing import Dict, Any
from backend.app_logging.logger import logger as app_logger

class EventProcessor:
    """
    CRIE Event Processor.
    Synchronizes Construction Risk Intelligence operations with application events
    (e.g., Project Created, Worker Added, Incident Logged, Safety Inspection Completed).
    """

    def process_event(self, event_type: str, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        project_id = event_payload.get("project_id", "UNKNOWN")
        app_logger.info(f"CRIE EventProcessor handling event '{event_type}' for project_id={project_id}")

        if event_type == "INCIDENT_LOGGED":
            scope = ["Insurance Agent", "Safety Agent"]
            analysis_type = "PARTIAL"
        elif event_type == "SAFETY_INSPECTION_COMPLETED":
            scope = ["Safety Agent"]
            analysis_type = "PARTIAL"
        elif event_type == "EQUIPMENT_STATUS_CHANGED":
            scope = ["Site Risk Agent"]
            analysis_type = "PARTIAL"
        else:
            scope = ["FULL"]
            analysis_type = "FULL"

        return {
            "event_type": event_type,
            "project_id": project_id,
            "recommended_scope": scope,
            "recommended_analysis_type": analysis_type,
            "status": "PROCESSED"
        }

event_processor = EventProcessor()
