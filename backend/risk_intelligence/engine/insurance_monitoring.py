import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.risk_intelligence.schemas.insurance_risk import (
    InsuranceMonitoringSession, InsuranceState, InsuranceFinding, InsuranceChangeRecord
)

class InsuranceMonitoringManager:
    """
    Insurance Monitoring Manager.
    Manages Insurance Monitoring Sessions, tracks policy and claim lifecycles,
    monitors Insurance Score movement, evaluates exposure trends (improving/stable/deteriorating),
    and maintains latest InsuranceState per project.
    """

    def __init__(self):
        self._active_sessions: Dict[str, List[InsuranceMonitoringSession]] = {}
        self._insurance_states: Dict[str, InsuranceState] = {}
        self._change_records: Dict[str, List[InsuranceChangeRecord]] = {}

    def create_monitoring_session(
        self,
        project_id: str,
        insurance_score: float,
        findings: List[Dict[str, Any]],
        policies_evaluated_count: int = 0,
        incidents_reviewed_count: int = 0,
        claims_reviewed_count: int = 0,
        assets_evaluated_count: int = 0
    ) -> InsuranceMonitoringSession:
        session_id = f"SESS_INS_{uuid.uuid4().hex[:8]}"

        finding_objs = [
            InsuranceFinding(
                category=f.get("category", "General Insurance Risk"),
                title=f.get("title", "Insurance Finding"),
                description=f.get("description", ""),
                severity=f.get("severity", "LOW"),
                policy_ref=f.get("policy_ref", "Commercial General Liability"),
                affected_asset=f.get("affected_asset"),
                evidence=f.get("evidence"),
                suggested_action=f.get("suggested_action", "Insurance mitigation action required"),
                priority=f.get("priority", "MEDIUM")
            )
            for f in findings
        ]

        session = InsuranceMonitoringSession(
            session_id=session_id,
            project_id=project_id,
            assessment_timestamp=datetime.utcnow(),
            policies_evaluated_count=policies_evaluated_count,
            incidents_reviewed_count=incidents_reviewed_count,
            claims_reviewed_count=claims_reviewed_count,
            assets_evaluated_count=assets_evaluated_count,
            insurance_score=insurance_score,
            findings=finding_objs,
            metadata={"session_mode": "SOFTWARE_INSURANCE_EXPOSURE_EVALUATION"}
        )

        if project_id not in self._active_sessions:
            self._active_sessions[project_id] = []

        previous_session = self._active_sessions[project_id][-1] if self._active_sessions[project_id] else None
        self._active_sessions[project_id].append(session)

        # Track Insurance Score movement & change record
        prev_score = previous_session.insurance_score if previous_session else insurance_score
        score_delta = insurance_score - prev_score
        if score_delta > 5.0:
            trend = "DETERIORATING"
            summary = f"Insurance risk exposure increased by {score_delta:.1f} pts"
        elif score_delta < -5.0:
            trend = "IMPROVING"
            summary = f"Insurance risk exposure decreased by {abs(score_delta):.1f} pts"
        else:
            trend = "STABLE"
            summary = "Insurance risk exposure score remains stable"

        change_rec = InsuranceChangeRecord(
            project_id=project_id,
            previous_score=prev_score,
            current_score=insurance_score,
            score_delta=score_delta,
            new_findings_count=len(finding_objs),
            resolved_findings_count=0,
            movement_summary=summary
        )

        if project_id not in self._change_records:
            self._change_records[project_id] = []
        self._change_records[project_id].append(change_rec)

        # Update InsuranceState
        critical_count = sum(1 for f in finding_objs if f.severity == "CRITICAL")
        health = "CRITICAL_EXPOSURE" if critical_count > 0 else ("ELEVATED_EXPOSURE" if insurance_score > 40.0 else "HEALTHY")
        claim_readiness = "CRITICAL_DOC_DEFICIENCY" if critical_count > 0 else ("DEFICIENT_DOCUMENTATION" if len(finding_objs) > 2 else "CLAIM_READY")

        state = InsuranceState(
            project_id=project_id,
            current_insurance_score=insurance_score,
            health_status=health,
            active_claims_count=claims_reviewed_count,
            critical_exposure_count=critical_count,
            claim_readiness_status=claim_readiness,
            exposure_trend=trend,
            last_session_id=session_id,
            last_evaluated_at=datetime.utcnow()
        )
        self._insurance_states[project_id] = state
        return session

    def get_insurance_state(self, project_id: str) -> Optional[InsuranceState]:
        return self._insurance_states.get(project_id)

    def get_session_history(self, project_id: str) -> List[InsuranceMonitoringSession]:
        return self._active_sessions.get(project_id, [])

    def get_change_records(self, project_id: str) -> List[InsuranceChangeRecord]:
        return self._change_records.get(project_id, [])

insurance_monitoring_manager = InsuranceMonitoringManager()
