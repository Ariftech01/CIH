from typing import Dict, Any
import time
from backend.risk_intelligence.agents.base_agent import BaseRiskAgent
from backend.risk_intelligence.schemas.agent import AgentResult
from backend.risk_intelligence.analyzers.reporting_analyzer import reporting_analyzer
from backend.risk_intelligence.integrations.reporting_export_adapter import reporting_export_adapter
from backend.risk_intelligence.engine.reporting_monitoring import reporting_session_manager
from backend.app_logging.logger import logger as app_logger

class ReportingAgent(BaseRiskAgent):
    """
    Enterprise Reporting Agent (RA).
    Consolidates analytical outputs from all Construction Risk Intelligence agents (Site Risk Agent, Safety Agent,
    Compliance Agent, Insurance Agent) into structured, executive-ready enterprise reports, operational summaries,
    audit documentation, and multi-channel export requests.
    Does NOT calculate risk or modify scores (weight = 0.0).
    """

    def __init__(self):
        super().__init__("Reporting Agent")
        self.analyzer = reporting_analyzer
        self.export_adapter = reporting_export_adapter
        self.session_manager = reporting_session_manager

    def analyze(self, project_context: Dict[str, Any]) -> AgentResult:
        start_time = time.time()
        project_id = project_context.get("project_id", "UNKNOWN_PROJECT")
        project_name = project_context.get("project_name", "Unknown Project")
        app_logger.info(f"ReportingAgent starting report generation for project_id={project_id}")

        report_type = project_context.get("report_type", "EXECUTIVE_RISK_SUMMARY")

        # 1. Generate Enterprise Report through ReportingAnalyzer
        enterprise_report = self.analyzer.generate_enterprise_report(project_context, report_type=report_type)
        report_id = enterprise_report["report_id"]

        # 2. Prepare Multi-Channel Export Request
        export_req = self.export_adapter.prepare_export_request(
            enterprise_report,
            export_format=project_context.get("export_format", "JSON"),
            destination=project_context.get("export_destination", "DASHBOARD"),
            classification=project_context.get("classification", "INTERNAL")
        )

        duration_ms = (time.time() - start_time) * 1000.0

        # 3. Create Report Generation Session & Update ReportState
        included_agents = list(project_context.get("component_scores", {}).keys())
        included_sections = [s["title"] for s in enterprise_report.get("sections", [])]

        session = self.session_manager.create_report_session(
            project_id=project_id,
            report_id=report_id,
            report_type=report_type,
            included_agents=included_agents,
            included_sections=included_sections,
            generation_duration_ms=duration_ms,
            quality_status="PASSED"
        )
        state = self.session_manager.get_report_state(project_id)

        summary_text = (
            f"Enterprise Report '{report_id}' ({report_type}) synthesized for {project_name}. "
            f"{len(included_sections)} sections generated across {len(included_agents)} agent domains."
        )

        return AgentResult(
            agent_name=self.name,
            status="SUCCESS",
            score=0.0,
            weight=0.0,
            summary=summary_text,
            findings={
                "report_id": report_id,
                "session_id": session.session_id,
                "report_type": report_type,
                "enterprise_report": enterprise_report,
                "export_request": export_req.model_dump(),
                "report_state": state.model_dump() if state else None,
                "sections_count": len(included_sections),
                "agents_count": len(included_agents)
            },
            recommendations=[]
        )
