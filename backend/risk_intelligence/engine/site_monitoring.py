import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.risk_intelligence.schemas.site_risk import SiteMonitoringSession, SiteState, SiteFinding

class SiteMonitoringManager:
    """
    Site Monitoring Manager.
    Manages Site Monitoring Sessions, tracks hazard evolution, monitors Site Risk Score movement,
    and maintains the latest SiteState for a construction project.
    """

    def __init__(self):
        self._active_sessions: Dict[str, List[SiteMonitoringSession]] = {}
        self._site_states: Dict[str, SiteState] = {}

    def create_monitoring_session(
        self,
        project_id: str,
        site_risk_score: float,
        findings: List[Dict[str, Any]],
        observed_count: int = 0
    ) -> SiteMonitoringSession:
        session_id = f"SESS_{uuid.uuid4().hex[:8]}"

        finding_objs = [
            SiteFinding(
                category=f.get("category", "General"),
                title=f.get("title", "Site Finding"),
                description=f.get("description", ""),
                severity=f.get("severity", "LOW"),
                location=f.get("location", "Site Zone"),
                evidence=f.get("evidence"),
                suggested_action=f.get("suggested_action", "Action required")
            )
            for f in findings
        ]

        session = SiteMonitoringSession(
            session_id=session_id,
            project_id=project_id,
            assessment_timestamp=datetime.utcnow(),
            observed_conditions_count=observed_count,
            hazards_detected_count=len(finding_objs),
            site_risk_score=site_risk_score,
            findings=finding_objs,
            metadata={"session_mode": "SOFTWARE_EVALUATION"}
        )

        if project_id not in self._active_sessions:
            self._active_sessions[project_id] = []
        self._active_sessions[project_id].append(session)

        # Update SiteState
        critical_count = sum(1 for f in finding_objs if f.severity == "CRITICAL")
        health = "CRITICAL" if critical_count > 0 else ("WARNING" if site_risk_score > 40.0 else "HEALTHY")

        state = SiteState(
            project_id=project_id,
            current_site_risk_score=site_risk_score,
            health_status=health,
            active_hazards_count=len(finding_objs),
            critical_hazards_count=critical_count,
            last_session_id=session_id,
            last_evaluated_at=datetime.utcnow()
        )
        self._site_states[project_id] = state
        return session

    def get_site_state(self, project_id: str) -> Optional[SiteState]:
        return self._site_states.get(project_id)

    def get_session_history(self, project_id: str) -> List[SiteMonitoringSession]:
        return self._active_sessions.get(project_id, [])

site_monitoring_manager = SiteMonitoringManager()
