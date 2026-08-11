from typing import Dict, Any
from backend.risk_intelligence.analyzers.reporting_analyzer import reporting_analyzer

class RiskReportBuilder:
    """
    Generates structured CRI report payloads independent of UI/presentation logic.
    Provides backwards compatibility for legacy build_executive_report while integrating
    with the enterprise ReportingAnalyzer pipeline.
    """

    @staticmethod
    def build_executive_report(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy compatibility method."""
        enterprise_report = reporting_analyzer.generate_enterprise_report(analysis_result, report_type="EXECUTIVE_RISK_SUMMARY")
        return {
            "title": f"Construction Risk Intelligence Report - Project {analysis_result.get('project_id')}",
            "overall_score": analysis_result.get("overall_risk_score"),
            "risk_level": analysis_result.get("risk_level"),
            "component_breakdown": analysis_result.get("component_scores"),
            "action_items": analysis_result.get("recommendations"),
            "generated_at": analysis_result.get("evaluated_at"),
            "enterprise_report": enterprise_report
        }
