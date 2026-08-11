from typing import Dict, Any
from backend.risk_intelligence.agents.base_agent import BaseRiskAgent
from backend.risk_intelligence.schemas.agent import AgentResult
from backend.risk_intelligence.analyzers.safety_analyzer import safety_analyzer
from backend.risk_intelligence.integrations.safety_data_adapter import safety_data_adapter
from backend.risk_intelligence.engine.safety_monitoring import safety_monitoring_manager
from backend.app_logging.logger import logger as app_logger

class SafetyAgent(BaseRiskAgent):
    """
    Enterprise Safety Agent (SA).
    Evaluates workforce safety conditions, PPE compliance, unsafe work practices,
    occupational hazard exposure, and near-miss history.
    Calculates a dedicated Safety Score, maintains Safety Monitoring Sessions & WorkforceSafetyState,
    and returns structured findings to CRIE without calculating overall project risk score or executing SQL.
    """

    def __init__(self):
        super().__init__("Safety Agent")
        self.analyzer = safety_analyzer
        self.adapter = safety_data_adapter
        self.monitoring_manager = safety_monitoring_manager

    def analyze(self, project_context: Dict[str, Any]) -> AgentResult:
        project_id = project_context.get("project_id", "UNKNOWN_PROJECT")
        app_logger.info(f"SafetyAgent starting workforce safety analysis for project_id={project_id}")

        # 1. Normalize data through Multi-Source Safety Adapter
        normalized_context = self.adapter.normalize_observations(project_context)

        # 2. Execute Deterministic Safety Analyzer & Rule Pipeline
        analysis_res = self.analyzer.analyze_safety_conditions(normalized_context)
        safety_score = analysis_res["safety_score"]
        findings = analysis_res["findings"]
        hazards = analysis_res["hazards"]
        worker_profiles = analysis_res["worker_profiles"]
        workgroup_profiles = analysis_res["workgroup_profiles"]
        metrics = analysis_res["metrics"]

        # 3. Create Safety Monitoring Session & Update WorkforceSafetyState
        session = self.monitoring_manager.create_monitoring_session(
            project_id=project_id,
            safety_score=safety_score,
            findings=findings,
            workers_evaluated_count=analysis_res["workers_evaluated_count"],
            observed_conditions_count=analysis_res["observed_conditions_count"]
        )

        critical_count = analysis_res["critical_hazards_count"]
        status_desc = "CRITICAL_SAFETY_BREACH" if critical_count > 0 else ("SAFETY_HAZARDS_DETECTED" if len(hazards) > 0 else "SAFE")

        summary_text = (
            f"Safety Score: {safety_score:.1f}/100 ({status_desc}). "
            f"{len(hazards)} hazards identified ({critical_count} critical). "
            f"{analysis_res['workers_evaluated_count']} workers evaluated."
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            score=safety_score,
            weight=1.5,
            summary=summary_text,
            findings={
                "safety_score": safety_score,
                "session_id": session.session_id,
                "status_description": status_desc,
                "total_hazards_count": analysis_res["total_hazards_count"],
                "critical_hazards_count": critical_count,
                "hazards": hazards,
                "findings": findings,
                "worker_profiles": worker_profiles,
                "workgroup_profiles": workgroup_profiles,
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
