import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models import (
    RiskAssessment,
    ProjectRiskScore,
    RiskRecommendation,
    IncidentRecord,
    SafetyAssessment,
    ComplianceAssessment,
    InsuranceAssessment,
    AgentExecution,
    RiskTrend,
    RiskSnapshot,
    NotificationLog,
    ExecutiveSummary,
    AuditRecord
)

class RiskRepository(BaseRepository[RiskAssessment]):
    """
    Data Access Repository for all Construction Risk Intelligence database entities.
    """

    def __init__(self, session: Session):
        super().__init__(RiskAssessment, session)

    # Risk Assessment Operations
    def create_assessment(
        self,
        project_id: str,
        assessment_type: str = "FULL",
        overall_score: float = 0.0,
        risk_level: str = "LOW",
        version: str = "1.0.0",
        summary: Optional[str] = None
    ) -> RiskAssessment:
        assessment = RiskAssessment(
            project_id=project_id,
            assessment_type=assessment_type,
            overall_risk_score=overall_score,
            risk_level=risk_level,
            version=version,
            summary=summary,
            status="COMPLETED",
            evaluated_at=datetime.utcnow()
        )
        self.session.add(assessment)
        self.session.flush()
        return assessment

    def get_latest_assessment(self, project_id: str) -> Optional[RiskAssessment]:
        stmt = (
            select(RiskAssessment)
            .where(RiskAssessment.project_id == project_id)
            .where(RiskAssessment.is_deleted == False)
            .order_by(desc(RiskAssessment.evaluated_at))
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def get_project_assessment_history(self, project_id: str, limit: int = 20) -> List[RiskAssessment]:
        stmt = (
            select(RiskAssessment)
            .where(RiskAssessment.project_id == project_id)
            .where(RiskAssessment.is_deleted == False)
            .order_by(desc(RiskAssessment.evaluated_at))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    # Component Risk Scores
    def save_component_score(
        self,
        assessment_id: str,
        project_id: str,
        category: str,
        score: float,
        weight: float = 1.0,
        status: str = "NORMAL",
        breakdown: Optional[Dict[str, Any]] = None
    ) -> ProjectRiskScore:
        score_obj = ProjectRiskScore(
            assessment_id=assessment_id,
            project_id=project_id,
            category=category,
            score=score,
            weight=weight,
            status=status,
            breakdown_json=json.dumps(breakdown) if breakdown else None,
            calculated_at=datetime.utcnow()
        )
        self.session.add(score_obj)
        self.session.flush()
        return score_obj

    # Recommendations
    def save_recommendation(
        self,
        assessment_id: str,
        project_id: str,
        category: str,
        title: str,
        description: str,
        suggested_action: str,
        priority: str = "MEDIUM",
        supporting_evidence: Optional[str] = None,
        is_ai_generated: bool = False
    ) -> RiskRecommendation:
        rec = RiskRecommendation(
            assessment_id=assessment_id,
            project_id=project_id,
            category=category,
            title=title,
            description=description,
            suggested_action=suggested_action,
            priority=priority,
            supporting_evidence=supporting_evidence,
            is_ai_generated=is_ai_generated,
            resolution_status="OPEN"
        )
        self.session.add(rec)
        self.session.flush()
        return rec

    def get_active_recommendations(self, project_id: str) -> List[RiskRecommendation]:
        stmt = (
            select(RiskRecommendation)
            .where(RiskRecommendation.project_id == project_id)
            .where(RiskRecommendation.resolution_status == "OPEN")
            .where(RiskRecommendation.is_deleted == False)
            .order_by(desc(RiskRecommendation.created_at))
        )
        return list(self.session.execute(stmt).scalars().all())

    # Incidents
    def save_incident(
        self,
        project_id: str,
        incident_type: str,
        title: str,
        description: str,
        severity: str = "MEDIUM",
        worker_id: Optional[str] = None,
        equipment_id: Optional[str] = None,
        location: Optional[str] = None,
        financial_impact: float = 0.0,
        corrective_action: Optional[str] = None
    ) -> IncidentRecord:
        incident = IncidentRecord(
            project_id=project_id,
            incident_type=incident_type,
            title=title,
            description=description,
            severity=severity,
            worker_id=worker_id,
            equipment_id=equipment_id,
            location=location,
            financial_impact=financial_impact,
            corrective_action=corrective_action,
            status="OPEN",
            incident_date=datetime.utcnow()
        )
        self.session.add(incident)
        self.session.flush()
        return incident

    def get_project_incidents(self, project_id: str) -> List[IncidentRecord]:
        stmt = (
            select(IncidentRecord)
            .where(IncidentRecord.project_id == project_id)
            .where(IncidentRecord.is_deleted == False)
            .order_by(desc(IncidentRecord.incident_date))
        )
        return list(self.session.execute(stmt).scalars().all())

    # Agent Execution Tracing
    def log_agent_execution(
        self,
        assessment_id: str,
        agent_name: str,
        status: str,
        duration_ms: float,
        summary: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> AgentExecution:
        execution = AgentExecution(
            assessment_id=assessment_id,
            agent_name=agent_name,
            execution_status=status,
            duration_ms=duration_ms,
            output_summary=summary,
            error_message=error_message,
            executed_at=datetime.utcnow()
        )
        self.session.add(execution)
        self.session.flush()
        return execution

    # Snapshots & Trends
    def create_snapshot(
        self,
        project_id: str,
        tag: str,
        overall_score: float,
        snapshot_data: Dict[str, Any],
        assessment_id: Optional[str] = None
    ) -> RiskSnapshot:
        snapshot = RiskSnapshot(
            project_id=project_id,
            assessment_id=assessment_id,
            snapshot_tag=tag,
            overall_score=overall_score,
            snapshot_data_json=json.dumps(snapshot_data),
            captured_at=datetime.utcnow()
        )
        self.session.add(snapshot)
        self.session.flush()
        return snapshot

    # Executive Summaries
    def save_executive_summary(
        self,
        assessment_id: str,
        project_id: str,
        headline: str,
        summary_text: str,
        key_findings: Optional[Dict[str, Any]] = None,
        author_type: str = "CIH_AI"
    ) -> ExecutiveSummary:
        summary_obj = ExecutiveSummary(
            assessment_id=assessment_id,
            project_id=project_id,
            headline=headline,
            summary_text=summary_text,
            key_findings_json=json.dumps(key_findings) if key_findings else None,
            author_type=author_type,
            generated_at=datetime.utcnow()
        )
        self.session.add(summary_obj)
        self.session.flush()
        return summary_obj

    # Audit Trail
    def log_audit(
        self,
        action: str,
        entity_type: str,
        project_id: Optional[str] = None,
        performed_by: Optional[str] = None,
        entity_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditRecord:
        audit = AuditRecord(
            project_id=project_id,
            action=action,
            performed_by=performed_by,
            entity_type=entity_type,
            entity_id=entity_id,
            details_json=json.dumps(details) if details else None,
            timestamp=datetime.utcnow()
        )
        self.session.add(audit)
        self.session.flush()
        return audit
