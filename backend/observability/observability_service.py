import time
import uuid
from typing import Dict, Any, List
from backend.app_logging.logger import logger
from backend.database.manager import db_manager
from backend.config.settings import settings

class ObservabilityService:
    """
    Centralized Observability Layer collecting logs, metrics, telemetry, and health diagnostics.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ObservabilityService, cls).__new__(cls)
            cls._instance._start_time = time.time()
            cls._instance._request_count = 0
            cls._instance._telemetry_events: List[Dict[str, Any]] = []
        return cls._instance

    def generate_correlation_id(self) -> str:
        return f"corr-{uuid.uuid4().hex[:8]}"

    def log_event(self, category: str, message: str, level: str = "INFO", project_id: str = None, correlation_id: str = None):
        cid = correlation_id or self.generate_correlation_id()
        structured_msg = f"[{category.upper()}] [CID: {cid}] {f'[Project: {project_id}] ' if project_id else ''}{message}"
        if level.upper() == "ERROR":
            logger.error(structured_msg)
        elif level.upper() == "WARNING":
            logger.warning(structured_msg)
        else:
            logger.info(structured_msg)

    def record_telemetry(self, feature_name: str, user_id: str = None, project_id: str = None, execution_time_ms: float = 0.0):
        self._request_count += 1
        entry = {
            "timestamp": time.time(),
            "feature": feature_name,
            "user_id": user_id,
            "project_id": project_id,
            "duration_ms": execution_time_ms
        }
        self._telemetry_events.append(entry)
        if len(self._telemetry_events) > 500:
            self._telemetry_events.pop(0)

    def get_system_diagnostics(self) -> Dict[str, Any]:
        uptime_seconds = round(time.time() - self._start_time, 2)
        db_health = db_manager.check_health()
        return {
            "uptime_seconds": uptime_seconds,
            "total_requests_processed": self._request_count,
            "environment": settings.APP_ENV,
            "database": db_health,
            "telemetry_event_count": len(self._telemetry_events),
            "services": {
                "workflow_engine": "Healthy",
                "analytics_engine": "Healthy",
                "notification_service": "Healthy",
                "ai_service": "Healthy"
            }
        }

observability_service = ObservabilityService()
