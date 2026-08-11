from typing import Dict, Any
from backend.risk_intelligence.agents.base_agent import BaseRiskAgent
from backend.risk_intelligence.schemas.agent import AgentResult
from backend.risk_intelligence.analyzers.site_risk_analyzer import site_risk_analyzer
from backend.risk_intelligence.integrations.site_data_adapter import site_data_adapter
from backend.risk_intelligence.engine.site_monitoring import site_monitoring_manager
from backend.app_logging.logger import logger as app_logger

class SiteRiskAgent(BaseRiskAgent):
    """
    Enterprise Site Risk Agent (SRA).
    Evaluates physical construction site conditions, applies deterministic SiteRules,
    identifies operational hazards, calculates Site Risk Score, creates Site Monitoring Sessions,
    and returns structured findings to CRIE without calculating overall project risk score or executing direct SQL.
    """

    def __init__(self):
        super().__init__("Site Risk Agent")
        self.analyzer = site_risk_analyzer
        self.adapter = site_data_adapter
        self.monitoring_manager = site_monitoring_manager

    def analyze(self, project_context: Dict[str, Any]) -> AgentResult:
        project_id = project_context.get("project_id", "UNKNOWN")
        app_logger.info(f"SiteRiskAgent starting analysis for project_id={project_id}")

        # 1. Normalize data through Multi-Source Adapter
        normalized_context = self.adapter.normalize_observations(project_context)

        # 2. Run Site Risk Analyzer & Rule Evaluations
        analysis_res = self.analyzer.analyze_site_conditions(normalized_context)
        site_risk_score = analysis_res["site_risk_score"]
        findings = analysis_res["findings"]
        hazards = analysis_res["hazards"]

        # 3. Register Site Monitoring Session
        session = self.monitoring_manager.create_monitoring_session(
            project_id=project_id,
            site_risk_score=site_risk_score,
            findings=findings,
            observed_count=normalized_context.get("observed_conditions_count", 0)
        )

        status_desc = "CRITICAL_HAZARDS" if analysis_res["critical_hazards_count"] > 0 else ("HAZARDS_DETECTED" if len(hazards) > 0 else "SAFE")

        summary_text = (
            f"Site Risk Score: {site_risk_score:.1f}/100 ({status_desc}). "
            f"{len(hazards)} hazards identified ({analysis_res['critical_hazards_count']} critical)."
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            score=site_risk_score,
            weight=1.2,
            summary=summary_text,
            findings={
                "site_risk_score": site_risk_score,
                "session_id": session.session_id,
                "status_description": status_desc,
                "total_hazards_count": analysis_res["total_hazards_count"],
                "critical_hazards_count": analysis_res["critical_hazards_count"],
                "hazards": hazards,
                "findings": findings
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
