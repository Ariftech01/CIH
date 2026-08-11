"""
Enterprise Dashboard Visual Component Library for Construction Risk Intelligence Hub.
Provides standardized, reusable UI rendering components for Streamlit dashboards
while preserving dark glassmorphism design language, blue branding, and zero risk calculation logic.
"""

import streamlit as st
from typing import Dict, Any, List, Union
from utils.styles import render_glass_card, render_kpi_card, render_progress_bar

def render_unified_risk_scorecard(overall_score: float, risk_level: str, health_status: str, health_index: float) -> None:
    """Renders high-level Unified Risk & Project Health Scorecard."""
    level_color = "#EF4444" if overall_score > 50 else ("#F59E0B" if overall_score > 25 else "#22C55E")
    badge_type = "danger" if overall_score > 50 else ("warning" if overall_score > 25 else "success")

    scorecard_html = f"""
    <div class="cih-glass-card" style="border-left: 6px solid {level_color}; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600;">Overall Construction Risk Score</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: var(--text-primary); margin-top: 0.2rem;">
                    {overall_score:.1f}<span style="font-size: 1.1rem; color: var(--text-secondary);">/100</span>
                    <span class="cih-badge cih-badge-{badge_type}" style="margin-left: 10px; font-size: 0.85rem; vertical-align: middle;">{risk_level} RISK</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600;">Project Health Index</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #22C55E; margin-top: 0.2rem;">
                    {health_index:.1f}% <span style="font-size: 0.9rem; font-weight: 500; color: var(--text-secondary);">({health_status})</span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(scorecard_html, unsafe_allow_html=True)

def render_agent_matrix_cards(component_scores: Dict[str, Any]) -> None:
    """Renders 5-Agent Risk Matrix Cards (Site, Safety, Compliance, Insurance, Reporting)."""
    if not component_scores:
        return

    cols = st.columns(min(len(component_scores), 5))
    icon_map = {
        "Site Risk": "🏗️",
        "Site": "🏗️",
        "Safety": "🦺",
        "Compliance": "📜",
        "Insurance": "🛡️",
        "Reporting": "📋"
    }

    for col, (comp_name, comp_data) in zip(cols, component_scores.items()):
        with col:
            score = float(comp_data.get("score", 0.0)) if isinstance(comp_data, dict) else float(getattr(comp_data, "score", 0.0))
            weight = float(comp_data.get("weight", 1.0)) if isinstance(comp_data, dict) else float(getattr(comp_data, "weight", 1.0))
            icon = icon_map.get(comp_name, "🔍")
            color = "#EF4444" if score > 50 else ("#F59E0B" if score > 25 else ("#3B82F6" if comp_name == "Reporting" else "#22C55E"))
            delta_str = f"Weight: {weight:.1f}" if weight > 0 else "Enterprise Log"
            render_kpi_card(f"{comp_name} Score", f"{score:.1f}/100", icon, delta_str, color)

def render_executive_alerts(alerts: List[Any]) -> None:
    """Renders Critical Risk Alerts Panel supporting both Pydantic models and dictionaries."""
    if not alerts:
        render_glass_card("🚨 Critical Risk Alerts", "<div style='color: var(--text-secondary); font-size: 0.9rem;'>Zero critical risk alerts detected across active agent monitoring sessions.</div>")
        return

    alert_html = ""
    for a in alerts[:5]:
        severity = getattr(a, "severity", a.get("severity", "HIGH") if isinstance(a, dict) else "HIGH")
        category = getattr(a, "category", a.get("category", "RISK") if isinstance(a, dict) else "RISK")
        title = getattr(a, "title", a.get("title", "Critical Hazard") if isinstance(a, dict) else "Critical Hazard")
        description = getattr(a, "description", a.get("description", "") if isinstance(a, dict) else "")
        action = getattr(a, "action", a.get("action", a.get("suggested_action", "")) if isinstance(a, dict) else "")

        severity_badge = "danger" if severity in ["CRITICAL", "HIGH"] else "warning"
        alert_html += f"""
        <div class="cih-activity-item" style="border-left: 3px solid #EF4444; padding-left: 10px; margin-bottom: 8px;">
            <div style="font-weight: 700; color: var(--text-primary); font-size: 0.92rem;">
                <span class="cih-badge cih-badge-{severity_badge}">{category.upper()}</span>
                {title}
            </div>
            <div class="cih-activity-text">{description}</div>
            <div class="cih-activity-time" style="color: #60A5FA; margin-top: 2px;">⚡ Action: {action}</div>
        </div>
        """
    render_glass_card(f"🚨 Critical Risk Alerts ({len(alerts)})", alert_html)

def render_executive_recommendation_panel(recommendations: List[Any]) -> None:
    """Renders Executive Action Plan Panel supporting both Pydantic models and dictionaries."""
    if not recommendations:
        return

    rec_html = ""
    for i, r in enumerate(recommendations[:4]):
        priority = getattr(r, "priority", r.get("priority", "MEDIUM") if isinstance(r, dict) else "MEDIUM")
        title = getattr(r, "title", r.get("title", "Recommendation") if isinstance(r, dict) else "Recommendation")
        description = getattr(r, "description", r.get("description", "") if isinstance(r, dict) else "")
        action = getattr(r, "action", (r.get("suggested_action") or r.get("action", "")) if isinstance(r, dict) else "")

        badge_type = "danger" if priority == "HIGH" else "info"
        rec_html += f"""
        <div class="cih-activity-item">
            <div style="font-weight: 600; color: var(--text-primary); font-size: 0.9rem;">
                {i+1}. {title}
                <span class="cih-badge cih-badge-{badge_type}" style="margin-left: 6px;">{priority}</span>
            </div>
            <div class="cih-activity-text" style="font-size: 0.85rem; color: var(--text-secondary);">{description}</div>
            <div class="cih-activity-time" style="color: #3B82F6; margin-top: 3px;">Suggested Action: {action}</div>
        </div>
        """
    render_glass_card("📋 Strategic & Operational Action Plan", rec_html)
