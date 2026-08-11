from typing import Dict, Any
from backend.risk_intelligence.agents.base_agent import BaseRiskAgent
from backend.risk_intelligence.schemas.agent import AgentResult
from backend.risk_intelligence.analyzers.compliance_analyzer import compliance_analyzer
from backend.risk_intelligence.integrations.compliance_data_adapter import compliance_data_adapter
from backend.risk_intelligence.engine.compliance_monitoring import compliance_monitoring_manager
from backend.app_logging.logger import logger as app_logger

class ComplianceAgent(BaseRiskAgent):
    """
    Enterprise Compliance Agent (CA).
    Evaluates building code regulations, permit status, inspection readiness,
    documentation completeness, certification validity, and audit preparedness.
    Calculates a dedicated Compliance Score, maintains Compliance Monitoring Sessions & GovernanceState,
    and returns structured findings to CRIE without calculating overall project risk score or executing SQL.
    """

    def __init__(self):
        super().__init__("Compliance Agent")
        self.analyzer = compliance_analyzer
        self.adapter = compliance_data_adapter
        self.monitoring_manager = compliance_monitoring_manager

    def analyze(self, project_context: Dict[str, Any]) -> AgentResult:
        project_id = project_context.get("project_id", "UNKNOWN_PROJECT")
        app_logger.info(f"ComplianceAgent starting regulatory compliance analysis for project_id={project_id}")

        # 1. Normalize data through Multi-Source Compliance Adapter
        normalized_context = self.adapter.normalize_observations(project_context)

        # 2. Execute Deterministic Compliance Analyzer & Rule Pipeline
        analysis_res = self.analyzer.analyze_compliance_conditions(normalized_context)
        compliance_score = analysis_res["compliance_score"]
        findings = analysis_res["findings"]
        hazards = analysis_res["hazards"]
        gov_profile = analysis_res["governance_profile"]
        contractor_profiles = analysis_res["contractor_profiles"]
        metrics = analysis_res["metrics"]

        # 3. Create Compliance Monitoring Session & Update GovernanceState
        session = self.monitoring_manager.create_monitoring_session(
            project_id=project_id,
            compliance_score=compliance_score,
            findings=findings,
            permits_evaluated_count=analysis_res["permits_evaluated_count"],
            inspections_reviewed_count=analysis_res["inspections_reviewed_count"],
            documents_verified_count=analysis_res["documents_verified_count"]
        )

        critical_count = analysis_res["critical_hazards_count"]
        status_desc = "CRITICAL_NON_COMPLIANCE" if critical_count > 0 else ("COMPLIANCE_ISSUES_DETECTED" if len(hazards) > 0 else "FULL_COMPLIANCE")

        summary_text = (
            f"Compliance Score: {compliance_score:.1f}/100 ({status_desc}). "
            f"{len(hazards)} compliance non-conformities identified ({critical_count} critical)."
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            score=compliance_score,
            weight=1.3,
            summary=summary_text,
            findings={
                "compliance_score": compliance_score,
                "session_id": session.session_id,
                "status_description": status_desc,
                "total_hazards_count": analysis_res["total_hazards_count"],
                "critical_hazards_count": critical_count,
                "hazards": hazards,
                "findings": findings,
                "governance_profile": gov_profile,
                "contractor_profiles": contractor_profiles,
                "metrics": metrics
            },
            recommendations=[
                {
                    "category": f["category"],
                    "title": f["title"],
                    "description": f["description"],
                    "suggested_action": f["suggested_action"],
                    "priority": "HIGH" if f["severity"] in ["HIGH", "CRITICAL"] else "MEDIUM"
                }
                for f in findings
            ]
        )
