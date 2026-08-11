from typing import Dict, Any, List
from datetime import datetime
from backend.risk_intelligence.integrations.base_adapter import BaseIntegrationAdapter

class SiteDataAdapter(BaseIntegrationAdapter):
    """
    Multi-Source Data Integration & Normalization Adapter for Site Risk Intelligence.
    Normalizes software records, manual site inspection forms, and provides extension points
    for future CCTV streams, drone visual feeds, IoT sensors, and weather APIs.
    """

    def __init__(self):
        super().__init__("Multi-Source Site Data Adapter")

    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        return {
            "source": self.name,
            "project_id": project_id,
            "cctv_streams": 0,
            "drone_feeds": 0,
            "iot_sensors": 0,
            "weather_condition": "NORMAL",
            "status": "READY"
        }

    def normalize_observations(self, raw_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms heterogeneous incoming data streams into standardized internal Business Context.
        """
        normalized = dict(raw_context)
        normalized["source_adapter"] = self.name
        normalized["normalized_at"] = datetime.utcnow().isoformat()

        # Format manual site inspection logs if provided
        manual_obs = raw_context.get("manual_observations", [])
        if manual_obs:
            normalized["observed_conditions_count"] = len(manual_obs)
        else:
            normalized["observed_conditions_count"] = 0

        return normalized

site_data_adapter = SiteDataAdapter()
