from typing import Dict, Any
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter

class DroneAdapter(BaseIntegrationAdapter):
    """
    Placeholder extension adapter for drone visual site inspection feeds.
    """
    def __init__(self):
        super().__init__("Drone Inspection Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "recent_flights": 0,
            "status": "STANDBY",
            "orthomosaic_available": False
        }
