from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.risk_intelligence.schemas.dashboard_risk import (
    DashboardContext, DashboardKPI, DashboardWidget
)
from backend.app_logging.logger import logger as app_logger

class DashboardContextBuilder:
    """
    Normalizes Construction Risk Intelligence Engine (CRIE) outputs into a standardized DashboardContext.
    Prepares executive KPIs, agent score matrix, critical alerts, and top recommendations
    for UI visualization without performing any risk analysis or score modifications.
    """

    def build_dashboard_context(self, crie_output: Dict[str, Any]) -> DashboardContext:
        project_id = crie_output.get("project_id", "UNKNOWN_PROJECT")
        project_name = crie_output.get("project_name", "Construction Project")
        overall_score = float(crie_output.get("overall_risk_score", 0.0))
        risk_level = crie_output.get("risk_level", "LOW")

        health_info = crie_output.get("project_health", {})
        health_status = health_info.get("status", "HEALTHY")
        health_index = float(health_info.get("health_index", 100.0))

        component_scores = crie_output.get("component_scores", {})
        recommendations = crie_output.get("recommendations", [])

        # Build Executive KPIs
        executive_kpis = [
            DashboardKPI(
                title="Overall Risk Score",
                value=f"{overall_score:.1f}/100",
                delta=f"Level: {risk_level}",
                icon="📊",
                color="#EF4444" if overall_score > 50 else ("#F59E0B" if overall_score > 25 else "#22C55E"),
                status=risk_level,
                category="OVERALL"
            ),
            DashboardKPI(
                title="Project Health Index",
                value=f"{health_index:.1f}/100",
                delta=health_status,
                icon="💚",
                color="#22C55E" if health_index > 75 else "#F59E0B",
                status=health_status,
                category="HEALTH"
            )
        ]

        # Add Component KPIs
        for comp_name, comp_data in component_scores.items():
            score = float(comp_data.get("score", 0.0))
            icon_map = {"Site": "🏗️", "Safety": "🦺", "Compliance": "📜", "Insurance": "🛡️", "Reporting": "📋"}
            icon = icon_map.get(comp_name, "🔍")
            color = "#EF4444" if score > 50 else ("#F59E0B" if score > 25 else "#3B82F6")
            executive_kpis.append(
                DashboardKPI(
                    title=f"{comp_name} Score",
                    value=f"{score:.1f}/100",
                    delta=f"Weight: {comp_data.get('weight', 1.0)}",
                    icon=icon,
                    color=color,
                    status="NORMAL",
                    category=comp_name.upper()
                )
            )

        # Extract Critical Alerts across agents
        critical_alerts: List[Dict[str, Any]] = []
        for comp_name, comp_data in component_scores.items():
            breakdown = comp_data.get("breakdown", {})
            hazards = breakdown.get("hazards", []) or breakdown.get("findings", [])
            for h in hazards:
                if isinstance(h, dict) and h.get("severity") in ["CRITICAL", "HIGH"]:
                    critical_alerts.append({
                        "category": comp_name,
                        "title": h.get("title", "Critical Hazard"),
                        "description": h.get("description", ""),
                        "severity": h.get("severity", "HIGH"),
                        "action": h.get("suggested_action", "Action required")
                    })

        # Format Top Recommendations
        formatted_recs: List[Dict[str, Any]] = [
            {
                "title": r.get("title", "Recommendation"),
                "description": r.get("description", ""),
                "action": r.get("suggested_action", ""),
                "priority": r.get("priority", "MEDIUM")
            }
            for r in recommendations[:5]
        ]

        dashboard_context = DashboardContext(
            project_id=project_id,
            project_name=project_name,
            overall_risk_score=overall_score,
            risk_level=risk_level,
            health_status=health_status,
            health_index=health_index,
            component_scores=component_scores,
            executive_kpis=executive_kpis,
            critical_alerts=critical_alerts,
            top_recommendations=formatted_recs,
            recent_activity=crie_output.get("recent_activity", []),
            historical_trends=crie_output.get("historical_trends", {}),
            timestamp=datetime.utcnow(),
            metadata={"builder": "DashboardContextBuilder"}
        )

        app_logger.info(f"DashboardContextBuilder assembled context for project '{project_id}' with {len(executive_kpis)} KPIs and {len(critical_alerts)} alerts.")
        return dashboard_context

dashboard_context_builder = DashboardContextBuilder()
