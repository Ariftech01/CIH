from typing import Dict, Any
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter

class IoTAdapter(BaseIntegrationAdapter):
    """
    Placeholder extension adapter for site IoT, RFID, GPS, and wearable sensor streams.
    """
    def __init__(self):
        super().__init__("IoT Sensor Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "connected_sensors": 0,
            "status": "STANDBY",
            "telemetry": {}
        }
