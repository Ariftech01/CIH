import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.risk_intelligence.schemas.reporting_risk import (
    ReportGenerationSession, ReportState, ReportChangeRecord
)

class ReportingSessionManager:
    """
    Reporting Session & Lifecycle Manager.
    Tracks Report Generation Sessions, maintains report version history,
    manages report lifecycle (Draft -> Generated -> Validated -> Approved -> Published -> Archived),
    and updates latest ReportState per project.
    """

    def __init__(self):
        self._active_sessions: Dict[str, List[ReportGenerationSession]] = {}
        self._report_states: Dict[str, ReportState] = {}
        self._change_records: Dict[str, List[ReportChangeRecord]] = {}

    def create_report_session(
        self,
        project_id: str,
        report_id: str,
        report_type: str = "EXECUTIVE_RISK_SUMMARY",
        included_agents: Optional[List[str]] = None,
        included_sections: Optional[List[str]] = None,
        generation_duration_ms: float = 0.0,
        quality_status: str = "PASSED"
    ) -> ReportGenerationSession:
        session_id = f"SESS_REP_{uuid.uuid4().hex[:8]}"

        session = ReportGenerationSession(
            session_id=session_id,
            project_id=project_id,
            report_id=report_id,
            generation_timestamp=datetime.utcnow(),
            report_type=report_type,
            included_agents=included_agents or [],
            included_sections=included_sections or [],
            generation_duration_ms=generation_duration_ms,
            status="GENERATED",
            metadata={"session_mode": "ENTERPRISE_REPORT_COMPOSITION"}
        )

        if project_id not in self._active_sessions:
            self._active_sessions[project_id] = []

        previous_session = self._active_sessions[project_id][-1] if self._active_sessions[project_id] else None
        self._active_sessions[project_id].append(session)

        # Track change record
        prev_report_id = previous_session.report_id if previous_session else None
        change_rec = ReportChangeRecord(
            project_id=project_id,
            previous_report_id=prev_report_id,
            current_report_id=report_id,
            sections_changed_count=len(included_sections or []),
            movement_summary=f"Report version generated ({report_type})"
        )

        if project_id not in self._change_records:
            self._change_records[project_id] = []
        self._change_records[project_id].append(change_rec)

        # Update ReportState
        current_state = self._report_states.get(project_id)
        pub_count = (current_state.published_count + 1) if current_state else 1

        state = ReportState(
            project_id=project_id,
            latest_report_id=report_id,
            health_status="HEALTHY",
            quality_status=quality_status,
            published_count=pub_count,
            archived_count=len(self._active_sessions[project_id]),
            last_generated_at=datetime.utcnow()
        )
        self._report_states[project_id] = state
        return session

    def get_report_state(self, project_id: str) -> Optional[ReportState]:
        return self._report_states.get(project_id)

    def get_session_history(self, project_id: str) -> List[ReportGenerationSession]:
        return self._active_sessions.get(project_id, [])

    def get_change_records(self, project_id: str) -> List[ReportChangeRecord]:
        return self._change_records.get(project_id, [])

reporting_session_manager = ReportingSessionManager()
