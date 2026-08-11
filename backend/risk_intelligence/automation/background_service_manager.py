from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import time
from backend.risk_intelligence.schemas.automation_risk import BackgroundJobSession
from backend.app_logging.logger import logger as app_logger

class BackgroundServiceManager:
    """
    Enterprise Background Service & Health Manager.
    Coordinates background housekeeping tasks (cache refresh, log maintenance, health monitoring),
    tracks background job execution sessions, and reports diagnostic health status.
    """

    def __init__(self):
        self._job_history: List[BackgroundJobSession] = []
        self._registered_services: Dict[str, Dict[str, Any]] = {
            "CRIE Risk Engine": {"status": "OPERATIONAL", "last_run": datetime.utcnow()},
            "Cache Housekeeping": {"status": "OPERATIONAL", "last_run": datetime.utcnow()},
            "Log Rotation": {"status": "OPERATIONAL", "last_run": datetime.utcnow()},
            "Health Monitor": {"status": "OPERATIONAL", "last_run": datetime.utcnow()}
        }

    def execute_background_job(self, service_name: str, job_func: Any, *args, **kwargs) -> BackgroundJobSession:
        job_id = f"JOB_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        status = "RUNNING"
        err_msg = None

        try:
            app_logger.info(f"BackgroundServiceManager starting background job '{job_id}' for service '{service_name}'")
            job_func(*args, **kwargs)
            status = "COMPLETED"
        except Exception as e:
            status = "FAILED"
            err_msg = str(e)
            app_logger.error(f"BackgroundServiceManager job '{job_id}' failed: {err_msg}")

        duration_ms = (time.time() - start_time) * 1000.0

        session = BackgroundJobSession(
            job_id=job_id,
            service_name=service_name,
            status=status,
            duration_ms=duration_ms,
            metadata={"error": err_msg} if err_msg else {},
            timestamp=datetime.utcnow()
        )

        self._job_history.append(session)
        if service_name in self._registered_services:
            self._registered_services[service_name]["last_run"] = datetime.utcnow()
            self._registered_services[service_name]["status"] = "OPERATIONAL" if status == "COMPLETED" else "DEGRADED"

        return session

    def get_system_health(self) -> Dict[str, Any]:
        """Returns diagnostic health status report of operational background services."""
        failed_count = sum(1 for s in self._job_history if s.status == "FAILED")
        overall_health = "CRITICAL" if failed_count > 3 else ("DEGRADED" if failed_count > 0 else "HEALTHY")

        return {
            "overall_health": overall_health,
            "services": self._registered_services,
            "total_jobs_executed": len(self._job_history),
            "failed_jobs_count": failed_count,
            "last_checked_at": datetime.utcnow().isoformat()
        }

background_service_manager = BackgroundServiceManager()
