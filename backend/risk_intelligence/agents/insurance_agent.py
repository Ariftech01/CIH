from typing import Dict, Any
from backend.risk_intelligence.agents.base_agent import BaseRiskAgent
from backend.risk_intelligence.schemas.agent import AgentResult
from backend.risk_intelligence.analyzers.insurance_analyzer import insurance_analyzer
from backend.risk_intelligence.integrations.insurance_data_adapter import insurance_data_adapter
from backend.risk_intelligence.engine.insurance_monitoring import insurance_monitoring_manager
from backend.app_logging.logger import logger as app_logger

class InsuranceAgent(BaseRiskAgent):
    """
    Enterprise Insurance Agent (IA).
    Evaluates insurance exposure, policy coverage, incident severity, asset protection,
    liability risk, and claim documentation readiness.
    Calculates a dedicated Insurance Score, maintains Insurance Monitoring Sessions & InsuranceState,
    and returns structured findings to CRIE without calculating overall project risk score or executing SQL.
    """

    def __init__(self):
        super().__init__("Insurance Agent")
        self.analyzer = insurance_analyzer
        self.adapter = insurance_data_adapter
        self.monitoring_manager = insurance_monitoring_manager

    def analyze(self, project_context: Dict[str, Any]) -> AgentResult:
        project_id = project_context.get("project_id", "UNKNOWN_PROJECT")
        app_logger.info(f"InsuranceAgent starting insurance exposure analysis for project_id={project_id}")

        # 1. Normalize data through Multi-Source Insurance Adapter
        normalized_context = self.adapter.normalize_observations(project_context)

        # 2. Execute Deterministic Insurance Analyzer & Rule Pipeline
        analysis_res = self.analyzer.analyze_insurance_conditions(normalized_context)
        insurance_score = analysis_res["insurance_score"]
        findings = analysis_res["findings"]
        hazards = analysis_res["hazards"]
        proj_profile = analysis_res["project_insurance_profile"]
        asset_profiles = analysis_res["asset_profiles"]
        metrics = analysis_res["metrics"]

        # 3. Create Insurance Monitoring Session & Update InsuranceState
        session = self.monitoring_manager.create_monitoring_session(
            project_id=project_id,
            insurance_score=insurance_score,
            findings=findings,
            policies_evaluated_count=analysis_res["policies_evaluated_count"],
            incidents_reviewed_count=analysis_res["incidents_reviewed_count"],
            claims_reviewed_count=analysis_res["claims_reviewed_count"],
            assets_evaluated_count=analysis_res["assets_evaluated_count"]
        )

        critical_count = analysis_res["critical_hazards_count"]
        status_desc = "CRITICAL_INSURANCE_EXPOSURE" if critical_count > 0 else ("INSURANCE_HAZARDS_DETECTED" if len(hazards) > 0 else "FULL_COVERAGE")

        summary_text = (
            f"Insurance Exposure Score: {insurance_score:.1f}/100 ({status_desc}). "
            f"{len(hazards)} insurance hazards identified ({critical_count} critical)."
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            score=insurance_score,
            weight=1.0,
            summary=summary_text,
            findings={
                "insurance_score": insurance_score,
                "session_id": session.session_id,
                "status_description": status_desc,
                "total_hazards_count": analysis_res["total_hazards_count"],
                "critical_hazards_count": critical_count,
                "hazards": hazards,
                "findings": findings,
                "project_insurance_profile": proj_profile,
                "asset_profiles": asset_profiles,
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
