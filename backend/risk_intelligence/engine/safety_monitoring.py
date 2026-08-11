import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.risk_intelligence.schemas.safety_risk import (
    SafetyMonitoringSession, WorkforceSafetyState, SafetyFinding, SafetyChangeRecord
)

class SafetyMonitoringManager:
    """
    Safety Monitoring Manager.
    Manages Safety Monitoring Sessions, tracks worker safety lifecycle, monitors Safety Score movement,
    evaluates score trends (improving/stable/deteriorating), and maintains latest WorkforceSafetyState per project.
    """

    def __init__(self):
        self._active_sessions: Dict[str, List[SafetyMonitoringSession]] = {}
        self._safety_states: Dict[str, WorkforceSafetyState] = {}
        self._change_records: Dict[str, List[SafetyChangeRecord]] = {}

    def create_monitoring_session(
        self,
        project_id: str,
        safety_score: float,
        findings: List[Dict[str, Any]],
        workers_evaluated_count: int = 0,
        observed_conditions_count: int = 0
    ) -> SafetyMonitoringSession:
        session_id = f"SESS_SAF_{uuid.uuid4().hex[:8]}"

        finding_objs = [
            SafetyFinding(
                category=f.get("category", "General Safety"),
                title=f.get("title", "Safety Finding"),
                description=f.get("description", ""),
                severity=f.get("severity", "LOW"),
                location=f.get("location", "General Work Zone"),
                worker_ref=f.get("worker_ref"),
                evidence=f.get("evidence"),
                suggested_action=f.get("suggested_action", "Safety action required"),
                priority=f.get("priority", "MEDIUM")
            )
            for f in findings
        ]

        session = SafetyMonitoringSession(
            session_id=session_id,
            project_id=project_id,
            assessment_timestamp=datetime.utcnow(),
            workers_evaluated_count=workers_evaluated_count,
            observed_conditions_count=observed_conditions_count,
            hazards_detected_count=len(finding_objs),
            safety_score=safety_score,
            findings=finding_objs,
            metadata={"session_mode": "SOFTWARE_WORKFORCE_SAFETY_EVALUATION"}
        )

        if project_id not in self._active_sessions:
            self._active_sessions[project_id] = []
        
        previous_session = self._active_sessions[project_id][-1] if self._active_sessions[project_id] else None
        self._active_sessions[project_id].append(session)

        # Track Safety Score movement & change record
        prev_score = previous_session.safety_score if previous_session else safety_score
        score_delta = safety_score - prev_score
        if score_delta > 5.0:
            trend = "DETERIORATING"
            summary = f"Safety risk increased by {score_delta:.1f} pts"
        elif score_delta < -5.0:
            trend = "IMPROVING"
            summary = f"Safety risk decreased by {abs(score_delta):.1f} pts"
        else:
            trend = "STABLE"
            summary = "Safety risk score remains stable"

        change_rec = SafetyChangeRecord(
            project_id=project_id,
            previous_score=prev_score,
            current_score=safety_score,
            score_delta=score_delta,
            new_findings_count=len(finding_objs),
            resolved_findings_count=0,
            movement_summary=summary
        )

        if project_id not in self._change_records:
            self._change_records[project_id] = []
        self._change_records[project_id].append(change_rec)

        # Update WorkforceSafetyState
        critical_count = sum(1 for f in finding_objs if f.severity == "CRITICAL")
        high_risk_count = sum(1 for f in finding_objs if f.severity in ["HIGH", "CRITICAL"])
        
        health = "CRITICAL" if critical_count > 0 else ("ELEVATED_RISK" if safety_score > 40.0 else "HEALTHY")

        state = WorkforceSafetyState(
            project_id=project_id,
            current_safety_score=safety_score,
            health_status=health,
            active_hazards_count=len(finding_objs),
            critical_hazards_count=critical_count,
            high_risk_workers_count=high_risk_count,
            high_risk_zones_count=1 if high_risk_count > 0 else 0,
            safety_trend=trend,
            last_session_id=session_id,
            last_evaluated_at=datetime.utcnow()
        )
        self._safety_states[project_id] = state
        return session

    def get_safety_state(self, project_id: str) -> Optional[WorkforceSafetyState]:
        return self._safety_states.get(project_id)

    def get_session_history(self, project_id: str) -> List[SafetyMonitoringSession]:
        return self._active_sessions.get(project_id, [])

    def get_change_records(self, project_id: str) -> List[SafetyChangeRecord]:
        return self._change_records.get(project_id, [])

safety_monitoring_manager = SafetyMonitoringManager()
