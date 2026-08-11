import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.risk_intelligence.schemas.compliance_risk import (
    ComplianceMonitoringSession, GovernanceState, ComplianceFinding, ComplianceChangeRecord
)

class ComplianceMonitoringManager:
    """
    Compliance Monitoring Manager.
    Manages Compliance Monitoring Sessions, tracks permit and certification lifecycles,
    monitors Compliance Score movement, evaluates regulatory trends (improving/stable/deteriorating),
    and maintains latest GovernanceState per project.
    """

    def __init__(self):
        self._active_sessions: Dict[str, List[ComplianceMonitoringSession]] = {}
        self._governance_states: Dict[str, GovernanceState] = {}
        self._change_records: Dict[str, List[ComplianceChangeRecord]] = {}

    def create_monitoring_session(
        self,
        project_id: str,
        compliance_score: float,
        findings: List[Dict[str, Any]],
        permits_evaluated_count: int = 0,
        inspections_reviewed_count: int = 0,
        documents_verified_count: int = 0
    ) -> ComplianceMonitoringSession:
        session_id = f"SESS_CMP_{uuid.uuid4().hex[:8]}"

        finding_objs = [
            ComplianceFinding(
                category=f.get("category", "General Regulatory Compliance"),
                title=f.get("title", "Compliance Finding"),
                description=f.get("description", ""),
                severity=f.get("severity", "MINOR"),
                regulation_ref=f.get("regulation_ref", "Building Code Regulations"),
                evidence=f.get("evidence"),
                suggested_action=f.get("suggested_action", "Compliance action required"),
                priority=f.get("priority", "MEDIUM")
            )
            for f in findings
        ]

        session = ComplianceMonitoringSession(
            session_id=session_id,
            project_id=project_id,
            assessment_timestamp=datetime.utcnow(),
            permits_evaluated_count=permits_evaluated_count,
            inspections_reviewed_count=inspections_reviewed_count,
            documents_verified_count=documents_verified_count,
            compliance_score=compliance_score,
            findings=finding_objs,
            metadata={"session_mode": "SOFTWARE_REGULATORY_COMPLIANCE_EVALUATION"}
        )

        if project_id not in self._active_sessions:
            self._active_sessions[project_id] = []

        previous_session = self._active_sessions[project_id][-1] if self._active_sessions[project_id] else None
        self._active_sessions[project_id].append(session)

        # Track Compliance Score movement & change record
        prev_score = previous_session.compliance_score if previous_session else compliance_score
        score_delta = compliance_score - prev_score
        if score_delta > 5.0:
            trend = "DETERIORATING"
            summary = f"Compliance risk increased by {score_delta:.1f} pts"
        elif score_delta < -5.0:
            trend = "IMPROVING"
            summary = f"Compliance risk decreased by {abs(score_delta):.1f} pts"
        else:
            trend = "STABLE"
            summary = "Compliance score remains stable"

        change_rec = ComplianceChangeRecord(
            project_id=project_id,
            previous_score=prev_score,
            current_score=compliance_score,
            score_delta=score_delta,
            new_findings_count=len(finding_objs),
            resolved_findings_count=0,
            movement_summary=summary
        )

        if project_id not in self._change_records:
            self._change_records[project_id] = []
        self._change_records[project_id].append(change_rec)

        # Update GovernanceState
        critical_count = sum(1 for f in finding_objs if f.severity == "CRITICAL")
        health = "CRITICAL_NON_COMPLIANCE" if critical_count > 0 else ("MINOR_NON_COMPLIANCE" if compliance_score > 40.0 else "HEALTHY")
        audit_status = "CRITICAL_DEFICIENCIES" if critical_count > 0 else ("MINOR_DEFICIENCIES" if len(finding_objs) > 2 else "AUDIT_READY")

        state = GovernanceState(
            project_id=project_id,
            current_compliance_score=compliance_score,
            health_status=health,
            active_violations_count=len(finding_objs),
            critical_violations_count=critical_count,
            audit_readiness_status=audit_status,
            regulatory_trend=trend,
            last_session_id=session_id,
            last_evaluated_at=datetime.utcnow()
        )
        self._governance_states[project_id] = state
        return session

    def get_governance_state(self, project_id: str) -> Optional[GovernanceState]:
        return self._governance_states.get(project_id)

    def get_session_history(self, project_id: str) -> List[ComplianceMonitoringSession]:
        return self._active_sessions.get(project_id, [])

    def get_change_records(self, project_id: str) -> List[ComplianceChangeRecord]:
        return self._change_records.get(project_id, [])

compliance_monitoring_manager = ComplianceMonitoringManager()
