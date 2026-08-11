"""About page module for CIH."""

import streamlit as st

from utils.styles import render_page_header


def render() -> None:
    """Render about page."""
    render_page_header("About", "Construction Intelligence Hub — Enterprise Platform")

    st.markdown(
        """
        <div class="cih-about-hero">
            <div style="font-size:4rem; margin-bottom:1rem;">🏗️</div>
            <h1 style="font-size:2.5rem; font-weight:800; color:var(--text-primary); margin:0;">
                Construction Intelligence Hub
            </h1>
            <p style="font-size:1.1rem; color:#3B82F6; margin-top:0.5rem; font-weight:600;">
                Enterprise Construction Management Platform
            </p>
            <div style="margin-top:2rem; display:flex; justify-content:center; gap:4rem; flex-wrap:wrap;">
                <div style="text-align:center;">
                    <div style="font-size:1.5rem; font-weight:700; color:var(--text-primary);">v1.0</div>
                    <div style="font-size:0.8rem; color:#64748B;">Version</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:1.5rem; font-weight:700; color:var(--text-primary);">Streamlit</div>
                    <div style="font-size:0.8rem; color:#64748B;">Framework</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="cih-glass-card">
                <div class="cih-card-title">📋 Project Overview</div>
                <p style="color:var(--text-secondary); line-height:1.7; font-size:0.9rem;">
                    Construction Intelligence Hub (CIH) is a centralized construction management platform
                    designed to streamline project operations, cost estimation, resource tracking, and
                    safety compliance. This frontend prototype demonstrates enterprise-grade UI/UX patterns
                    inspired by industry leaders like Autodesk Construction Cloud, Procore, and SAP Fiori.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="cih-glass-card">
                <div class="cih-card-title">🛠 Technology Stack</div>
                <div class="cih-metric-row"><span class="cih-metric-label">Language</span><span class="cih-metric-value">Python 3.10+</span></div>
                <div class="cih-metric-row"><span class="cih-metric-label">Frontend</span><span class="cih-metric-value">Streamlit</span></div>
                <div class="cih-metric-row"><span class="cih-metric-label">Charts</span><span class="cih-metric-value">Plotly</span></div>
                <div class="cih-metric-row"><span class="cih-metric-label">Data</span><span class="cih-metric-value">Pandas</span></div>
                <div class="cih-metric-row"><span class="cih-metric-label">Styling</span><span class="cih-metric-value">Custom CSS via Markdown</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    features = [
        ("📊", "Executive Dashboard", "Real-time KPIs, charts, and operational insights"),
        ("📁", "Project Management", "Full project lifecycle tracking and management"),
        ("💰", "Cost Estimation", "Enterprise-grade construction cost calculator"),
        ("🧱", "Material Management", "Inventory tracking with stock alerts"),
        ("👷", "Worker Management", "Workforce attendance and performance analytics"),
        ("🦺", "Safety Monitoring", "Compliance checklists and incident tracking"),
        ("🚜", "Equipment Tracking", "Fleet health and maintenance monitoring"),
        ("📈", "Progress Monitoring", "Milestone tracking with Gantt visualization"),
        ("📄", "Reports", "Multi-format report generation and export"),
    ]

    feat_cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with feat_cols[i % 3]:
            st.markdown(
                f"""
                <div class="cih-glass-card" style="min-height:120px;">
                    <div style="font-size:1.5rem; margin-bottom:0.5rem;">{icon}</div>
                    <div class="cih-card-title" style="font-size:0.95rem;">{title}</div>
                    <p style="color:#64748B; font-size:0.8rem; margin:0;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="text-align:center; margin-top:2rem; padding:1.5rem; color:#64748B; font-size:0.85rem;">
            Frontend Prototype · Developed using Streamlit · © 2026 Construction Intelligence Hub
        </div>
        """,
        unsafe_allow_html=True,
    )
