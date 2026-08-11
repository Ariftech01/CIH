from typing import Dict, Any

class RiskDashboardDataProvider:
    """
    Formats CRI data into structured dictionary payloads ready for dashboard consumption.
    No Streamlit or UI component code resides here.
    """

    @staticmethod
    def format_dashboard_summary(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "summary_card": {
                "overall_score": analysis_result.get("overall_risk_score", 0.0),
                "risk_level": analysis_result.get("risk_level", "UNKNOWN"),
                "total_recommendations": len(analysis_result.get("recommendations", []))
            },
            "component_cards": analysis_result.get("component_scores", {}),
            "recommendation_list": analysis_result.get("recommendations", []),
            "agent_statuses": [
                {"agent": a.get("agent_name"), "status": a.get("status"), "duration_ms": a.get("duration_ms")}
                for a in analysis_result.get("agent_results", [])
            ]
        }
