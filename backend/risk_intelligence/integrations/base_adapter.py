from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseIntegrationAdapter(ABC):
    """
    Abstract adapter for hardware, IoT sensors, weather APIs, CCTV, drone visual feeds, and external enterprise systems.
    Provides extension points for future enterprise hardware integrations.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fetch_data(self, project_id: str) -> Dict[str, Any]:
        """Fetch and standardize data from external source into unified dictionary."""
        pass
