from typing import Dict, Any
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter

class WeatherAdapter(BaseIntegrationAdapter):
    """
    Placeholder extension adapter for external weather APIs and site environmental monitoring.
    """
    def __init__(self):
        super().__init__("Weather API Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "condition": "CLEAR",
            "temperature_c": 24.0,
            "wind_speed_kmh": 12.0,
            "weather_risk_level": "LOW"
        }
