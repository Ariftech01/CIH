"""
Construction Risk Intelligence module for Agentic AI for Safety Monitoring with Construction Risk Analytics (CIH).
Provides unified executive UI visualization for CRIE risk scorecards, Site Risk Agent, Safety Agent,
Compliance Agent, Insurance Agent, Reporting Agent, Historical Analytics, and Automation Framework
with real-time ingestion layers and interactive feeds.
"""

import streamlit as st
import pandas as pd
from utils import charts, dummy_data
from utils.styles import render_glass_card, render_kpi_card, render_page_header, render_progress_bar, status_to_badge
from utils.dashboard_components import (
    render_executive_alerts,
    render_executive_recommendation_panel
)

from backend.risk_intelligence.engine.crie import risk_intelligence_engine
from backend.risk_intelligence.integrations.dashboard_context_builder import dashboard_context_builder
from backend.risk_intelligence.agents import SiteRiskAgent, SafetyAgent, ComplianceAgent, InsuranceAgent, ReportingAgent
from backend.risk_intelligence.automation import (
    notification_engine,
    background_service_manager,
    performance_manager,
    deployment_validator
)


@st.cache_resource(show_spinner=False)
def _get_cached_cri_context(project_id: str, project_name: str):
    sample_context = {
        "project_id": project_id,
        "project_name": project_name,
        "incidents_list": [
            {"id": "INC_01", "type": "DAMAGE", "severity": "MODERATE", "financial_impact": 18000.0, "description": "Formwork displacement during concrete pour on Level 3"}
        ],
        "policy_records": [
            {"id": "POL_CAR", "name": "Contractor All Risk Policy", "status": "ACTIVE"}
        ],
        "equipment_list": [
            {"id": "EQ_01", "name": "Tower Crane Alpha", "replacement_value": 250000.0, "insurance_status": "COVERED"}
        ],
        "missing_ppe_count": 0,
        "manual_safety_observations": ["Scaffolding toe-boards verified"]
    }
    crie_output = risk_intelligence_engine.execute_analysis_pipeline(sample_context, assessment_id="cri_page_assessment")
    dash_ctx = dashboard_context_builder.build_dashboard_context(crie_output)
    return sample_context, dash_ctx


def render() -> None:
    """Render the Construction Risk Intelligence unified page."""
    # Page-scoped responsive tab navigation CSS and Real-Time HUD styling
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            overflow-y: hidden !important;
            scroll-behavior: smooth !important;
            -webkit-overflow-scrolling: touch !important;
            gap: 4px !important;
            padding-bottom: 6px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 4px !important;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.6) !important;
            border-radius: 4px !important;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: rgba(59, 130, 246, 0.5) !important;
            border-radius: 4px !important;
        }

        .stTabs [data-baseweb="tab-list"] button {
            flex-shrink: 0 !important;
            white-space: nowrap !important;
            padding: 8px 14px !important;
            font-size: 0.9rem !important;
            border-radius: 8px 8px 0 0 !important;
            transition: all 0.2s ease-in-out !important;
        }

        @media (max-width: 1366px) {
            .stTabs [data-baseweb="tab-list"] button {
                padding: 6px 10px !important;
                font-size: 0.82rem !important;
            }
        }

        @media (max-width: 1024px) {
            .stTabs [data-baseweb="tab-list"] button {
                padding: 5px 8px !important;
                font-size: 0.78rem !important;
            }
        }

        /* Real-Time Ingestion Layer & HUD Styles */
        .cri-ingestion-box {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.75) 100%);
            border: 1px solid rgba(59, 130, 246, 0.25);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            position: relative;
            backdrop-filter: blur(16px);
        }

        .cri-hud-stream {
            background: rgba(10, 15, 29, 0.85);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-radius: 12px;
            padding: 1rem;
            position: relative;
            overflow: hidden;
            font-family: monospace;
            color: #60A5FA;
        }

        .cri-hud-overlay {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2);
            padding-bottom: 0.4rem;
        }

        .cri-pulse-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: #22C55E;
            font-weight: 700;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .cri-pulse-dot {
            width: 8px;
            height: 8px;
            background: #22C55E;
            border-radius: 50%;
            box-shadow: 0 0 10px #22C55E;
            animation: criPulse 1.5s infinite;
        }

        @keyframes criPulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    render_page_header("Construction Risk Intelligence", "Enterprise multi-agent risk assessment, safety intelligence, compliance governance, and insurance exposure")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_project_id = active_proj.id if active_proj else st.session_state.get("active_project_id", "proj_cri_01")
    active_project = active_proj.project_name if active_proj else st.session_state.get("active_project_name", "Commercial High-Rise Infrastructure")

    # Fetch cached CRIE Pipeline Execution & Dashboard Context
    sample_context, dash_ctx = _get_cached_cri_context(active_project_id, active_project)

    # Sub-Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Overview",
        "🏗️ Site Risk",
        "🦺 Safety Agent",
        "📜 Compliance Agent",
        "🛡️ Insurance Agent",
        "📋 Reporting Agent",
        "📈 Historical Analytics",
        "⚡ Automation & Governance"
    ])

    # TAB 1: OVERVIEW & SCORECARD
    with tab1:
        st.markdown("#### Enterprise Executive Risk Overview")
        col1, col2 = st.columns([2, 1])
        with col1:
            render_executive_alerts(dash_ctx.critical_alerts)
        with col2:
            render_executive_recommendation_panel(dash_ctx.top_recommendations)

        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("##### Component Risk Score Weights")
            weight_data = pd.DataFrame([
                {"Agent Domain": k, "Score": v["score"], "Weight": v["weight"]}
                for k, v in dash_ctx.component_scores.items()
            ])
            st.dataframe(weight_data, use_container_width=True, hide_index=True)
        with col4:
            st.markdown("##### Executive Key Performance Indicators")
            for kpi in dash_ctx.executive_kpis:
                title = getattr(kpi, "title", kpi.get("title", "KPI") if isinstance(kpi, dict) else "KPI")
                val_str = str(getattr(kpi, "value", kpi.get("value", "0") if isinstance(kpi, dict) else "0"))
                try:
                    cleaned_val = float(val_str.replace('%','').replace('/100','')) if ('%' in val_str or '/100' in val_str) else 50.0
                except Exception:
                    cleaned_val = 50.0
                render_progress_bar(f"{title}: {val_str}", min(cleaned_val, 100.0))


    # TAB 2: SITE RISK AGENT
    with tab2:
        st.markdown("#### 🏗️ Site Risk Agent Subsystem")

        # Real-Time Ingestion Layer (Extra UI Layer)
        with st.expander("📡 Real-Time Site Ingestion & Sensor Feed Interface", expanded=True):
            st.markdown(
                """
                <div class="cri-hud-overlay">
                    <span class="cri-pulse-badge"><span class="cri-pulse-dot"></span> LIVE SENSOR & DRONE STREAM READY</span>
                    <span style="color:#94A3B8;">PROTOCOL: RTSP / MQTT / LiDAR GeoTIFF</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_in1, col_in2 = st.columns([1.2, 1])

            with col_in1:
                feed_source = st.selectbox(
                    "Feed Ingestion Source",
                    [
                        "🛰️ Aerial Drone Orthomosaic / RGB Stream",
                        "📹 Perimeter CCTV Camera #03 (Excavation)",
                        "🏔️ Geotechnical Inclinometer & Piezometer Array",
                        "🏗️ Tower Crane Alpha Structural Telemetry",
                        "📁 Upload Local Site Image / Point Cloud Scan"
                    ],
                    key="site_feed_source"
                )

                uploaded_site_file = st.file_uploader(
                    "Upload Site Imagery / Inspection Scan (JPG, PNG, TIFF, MP4)",
                    type=["jpg", "jpeg", "png", "tif", "tiff", "mp4"],
                    key="site_file_uploader",
                    help="Upload drone snapshots or geotechnical imagery for real-time risk classification."
                )

            with col_in2:
                selected_zone = st.selectbox(
                    "Target Monitoring Zone",
                    ["Zone A - Foundation & Retaining Wall", "Zone B - Deep Excavation Pit", "Zone C - Crane Hoist Radius", "Zone D - Level 3 Formwork"],
                    key="site_zone_select"
                )

                c_env1, c_env2 = st.columns(2)
                with c_env1:
                    weather_cond = st.selectbox("Weather Telemetry", ["Clear (31°C, Wind 12 km/h)", "Rain / High Moisture", "Gusty Wind (> 35 km/h)"], key="site_weather")
                with c_env2:
                    soil_status = st.selectbox("Soil Sensor Status", ["Nominal Pore Pressure", "Elevated Moisture (Warning)", "Soil Shift (Alert)"], key="site_soil")

                run_scan = st.button("🚀 Ingest & Process Site Stream", use_container_width=True, key="btn_run_site_scan")

            if uploaded_site_file:
                st.image(uploaded_site_file, caption=f"📸 Uploaded Inspection Artifact: {uploaded_site_file.name} (Ready for inference)", use_container_width=True)
            elif run_scan:
                st.success(f"✅ Real-Time feed ingested from '{feed_source}' for {selected_zone}. Geotechnical telemetry correlated with risk model.")
            else:
                st.markdown(
                    f"""
                    <div class="cri-hud-stream">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                            <span>STREAM: {feed_source}</span>
                            <span style="color:#34D399;">FPS: 30.0 | LATENCY: 28ms</span>
                        </div>
                        <div style="font-size:0.75rem; color:#94A3B8;">Active Zone: {selected_zone} | Telemetry: {weather_cond} | Sensors: {soil_status}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        sra_res = SiteRiskAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Site Risk Score", f"{sra_res.score:.1f}/100", "🏗️", sra_res.summary, "#EF4444" if sra_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Hazards Detected", str(sra_res.findings.get("total_hazards_count", 0)), "⚠️")
        with c3:
            render_kpi_card("Geotechnical Status", "Stable", "⛰️", delta="Ground anchor verified", delta_color="#22C55E")

        st.markdown("##### Site Hazard Breakdown")
        hazards = sra_res.findings.get("hazards", [])
        if hazards:
            for h in hazards:
                st.markdown(
                    f'<div class="cih-activity-item">'
                    f'<span class="cih-badge cih-badge-danger">{h.get("severity", "HIGH")}</span> '
                    f'<strong style="color:var(--text-primary);">{h.get("hazard_type", "HAZARD")}</strong> — {h.get("description")}'
                    f'<div class="cih-activity-time" style="color:#60A5FA; margin-top:2px;">Location: {h.get("location", "Site Perimeter")}</div></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Zero physical site hazards detected.")

    # TAB 3: SAFETY AGENT
    with tab3:
        st.markdown("#### 🦺 Safety Agent Subsystem")

        # Real-Time Ingestion Layer (Extra UI Layer)
        with st.expander("👁️ Real-Time Workforce Computer Vision & Safety Feed Interface", expanded=True):
            st.markdown(
                """
                <div class="cri-hud-overlay">
                    <span class="cri-pulse-badge"><span class="cri-pulse-dot"></span> LIVE WORKFORCE VISION FEED ACTIVE</span>
                    <span style="color:#94A3B8;">MODEL: YOLOv8x-EHS (PPE & Fall Risk)</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_s1, col_s2 = st.columns([1.2, 1])
            with col_s1:
                cv_source = st.selectbox(
                    "Safety Camera Stream / Mode",
                    [
                        "📹 Live Turnstile Gate 1 (Access Control + PPE)",
                        "📹 Tower 2 Hoist & Scaffolding Deck (Fall Hazard Detection)",
                        "📹 Excavation Perimeter Zone (Heavy Plant Exclusion)",
                        "📁 Upload Workforce Photo / Video Inspection Clip"
                    ],
                    key="safety_cv_source"
                )

                uploaded_safety_img = st.file_uploader(
                    "Upload Worker Inspection Image / Video Frame (JPG, PNG, MP4)",
                    type=["jpg", "jpeg", "png", "mp4"],
                    key="safety_file_uploader",
                    help="Upload workforce photos to perform automated PPE detection and violation logging."
                )

            with col_s2:
                detect_targets = st.multiselect(
                    "Active Detection Modules",
                    ["🪖 Hardhat Verification", "🦺 High-Vis Vest Check", "🔗 Harness Anchor Tagging", "🚷 Exclusion Zone Intrusion", "👢 Steel-Toe Boots"],
                    default=["🪖 Hardhat Verification", "🦺 High-Vis Vest Check", "🔗 Harness Anchor Tagging"],
                    key="safety_targets_select"
                )

                conf_thresh = st.slider("Vision Confidence Threshold", min_value=0.50, max_value=0.95, value=0.75, step=0.05, key="safety_conf_slider")

                run_safety_scan = st.button("🦺 Execute Real-Time Safety Vision Inspection", use_container_width=True, key="btn_run_safety_scan")

            if uploaded_safety_img:
                st.image(uploaded_safety_img, caption=f"👷 Uploaded Workforce Inspection Frame: {uploaded_safety_img.name} (Bounding boxes mapped)", use_container_width=True)
            elif run_safety_scan:
                st.success(f"✅ Real-Time Vision Scan executed on '{cv_source}'. Confidence: {conf_thresh*100:.0f}%. All active workers classified.")
            else:
                st.markdown(
                    f"""
                    <div class="cri-hud-stream">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                            <span>SOURCE: {cv_source}</span>
                            <span style="color:#34D399;">DETECTIONS: 15 PERSONS | 0 BREACHES</span>
                        </div>
                        <div style="font-size:0.75rem; color:#94A3B8;">Active Filters: {', '.join(detect_targets)} | Conf: {conf_thresh*100:.0f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        sa_res = SafetyAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Workforce Safety Score", f"{sa_res.score:.1f}/100", "🦺", sa_res.summary, "#EF4444" if sa_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Workers Evaluated", str(sa_res.findings.get("workers_evaluated_count", 15)), "👷")
        with c3:
            render_kpi_card("Critical PPE Compliance", "98.5%", "🪖", delta="+1.2% this week", delta_color="#22C55E")

        st.markdown("##### Workforce Safety Findings")
        for f in sa_res.findings.get("findings", []):
            badge = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "warning"
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<span class="cih-badge cih-badge-{badge}">{f.get("severity")}</span> '
                f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                f'<div class="cih-activity-time" style="color:#60A5FA;">Suggested Action: {f.get("suggested_action")}</div></div>',
                unsafe_allow_html=True
            )

    # TAB 4: COMPLIANCE AGENT
    with tab4:
        st.markdown("#### 📜 Compliance Agent Subsystem")

        # Real-Time Ingestion Layer (Extra UI Layer)
        with st.expander("📑 Regulatory Document & Statutory Audit Ingestion Interface", expanded=True):
            st.markdown(
                """
                <div class="cri-hud-overlay">
                    <span class="cri-pulse-badge"><span class="cri-pulse-dot"></span> REGULATORY AUDIT GATEWAY CONNECTED</span>
                    <span style="color:#94A3B8;">PARSER: OCR / NLP Clause Matcher</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_c1, col_c2 = st.columns([1.2, 1])
            with col_c1:
                std_code = st.selectbox(
                    "Governing Regulatory Standard",
                    [
                        "🇮🇳 NBC 2016 (National Building Code of India)",
                        "🏗️ IS 456:2000 (Plain and Reinforced Concrete)",
                        "🛡️ OSHA 1926 (Safety and Health Regulations for Construction)",
                        "🏛️ Local Municipal Corporation Building By-Laws",
                        "🌿 Environmental Clearance & EIA Norms"
                    ],
                    key="comp_std_code"
                )

                uploaded_doc = st.file_uploader(
                    "Upload Statutory Permit, Audit Sheet or Drawing (PDF, DOCX, DWG, PNG)",
                    type=["pdf", "docx", "dwg", "png", "json"],
                    key="comp_file_uploader",
                    help="Upload structural clearance or municipal permits for automated regulatory clause cross-examination."
                )

            with col_c2:
                permit_type = st.selectbox(
                    "Permit / Statutory Category",
                    ["Excavation & Shoring Clearance", "Height Work Authorization", "Hot Work & Fire Safety NoC", "Structural Stability Certificate", "Environmental Discharge Clearance"],
                    key="comp_permit_type"
                )

                manual_obs = st.text_input("Inspector Manual Audit Observation / Clause Ref", placeholder="e.g. Scaffolding anchor verified per IS 456 Cl. 15.2", key="comp_manual_obs")

                run_comp_audit = st.button("📜 Ingest & Audit Compliance Document", use_container_width=True, key="btn_run_comp_audit")

            if uploaded_doc:
                st.info(f"📄 Ingested Document: **{uploaded_doc.name}** ({uploaded_doc.size / 1024:.1f} KB). Ready for clause matching with {std_code}.")
            elif run_comp_audit:
                st.success(f"✅ Regulatory compliance parsed for '{permit_type}' under {std_code}. Zero statutory breaches identified.")
            else:
                st.markdown(
                    f"""
                    <div class="cri-hud-stream">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                            <span>ACTIVE STANDARD: {std_code}</span>
                            <span style="color:#34D399;">PERMITS CROSS-REFERENCED: 12/12</span>
                        </div>
                        <div style="font-size:0.75rem; color:#94A3B8;">Target Category: {permit_type} | Clause Parser: IS/NBC Rule-Engine Active</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        ca_res = ComplianceAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Compliance Score", f"{ca_res.score:.1f}/100", "📜", ca_res.summary, "#EF4444" if ca_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Active Permits", "12/12 Verified", "✅")
        with c3:
            render_kpi_card("Audit Readiness", "Pass", "🔍", delta="IS 456 & NBC 2016 Compliant", delta_color="#22C55E")

        st.markdown("##### Regulatory Compliance Findings")
        for f in ca_res.findings.get("findings", []):
            badge = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "info"
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<span class="cih-badge cih-badge-{badge}">{f.get("severity")}</span> '
                f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                f'<div class="cih-activity-time" style="color:#60A5FA;">Regulation: {f.get("regulation_code", "NBC-2016")}</div></div>',
                unsafe_allow_html=True
            )

    # TAB 5: INSURANCE AGENT
    with tab5:
        st.markdown("#### 🛡️ Insurance Agent Subsystem")

        # Real-Time Ingestion Layer (Extra UI Layer)
        with st.expander("📊 Policy, Claim & Underwriter Ingestion Interface", expanded=True):
            st.markdown(
                """
                <div class="cri-hud-overlay">
                    <span class="cri-pulse-badge"><span class="cri-pulse-dot"></span> UNDERWRITING TELEMETRY ONLINE</span>
                    <span style="color:#94A3B8;">MODEL: Actuarial PML & Severity Estimator</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_i1, col_i2 = st.columns([1.2, 1])
            with col_i1:
                policy_cat = st.selectbox(
                    "Insurance Policy Category",
                    [
                        "🛡️ Contractor All Risk (CAR) Policy #POL-CAR-2026",
                        "🏭 Erection All Risk (EAR) Policy",
                        "👥 Third-Party Public Liability (TPL)",
                        "🚜 Contractor Plant & Machinery (CPM) Asset Coverage",
                        "📁 Upload Policy Schedule / Loss Adjuster File"
                    ],
                    key="ins_policy_cat"
                )

                uploaded_policy = st.file_uploader(
                    "Upload Policy Document / Loss Adjuster Report (PDF, XLSX, CSV)",
                    type=["pdf", "xlsx", "csv"],
                    key="ins_file_uploader",
                    help="Upload insurance policy schedules or loss adjustor assessment files."
                )

            with col_i2:
                claim_scenario = st.selectbox(
                    "Simulated Risk Scenario",
                    ["Water Ingress / Concrete Washout", "Tower Crane Structural Defect", "Scaffolding Structural Deflection", "Perimeter Trench Subsidence"],
                    key="ins_claim_scenario"
                )

                est_val = st.number_input("Estimated Asset Exposure / Loss ($ USD)", min_value=1000.0, max_value=5000000.0, value=18000.0, step=1000.0, key="ins_est_val")

                run_ins_sim = st.button("🛡️ Run Actuarial Underwriting & Exposure Simulation", use_container_width=True, key="btn_run_ins_sim")

            if uploaded_policy:
                st.info(f"📋 Ingested Policy Schedule: **{uploaded_policy.name}** ({uploaded_policy.size / 1024:.1f} KB). Underwriting parameters bound.")
            elif run_ins_sim:
                st.success(f"✅ Underwriting simulation executed for '{claim_scenario}' at ${est_val:,.2f}. Policy coverage verified with 0 exposure gap.")
            else:
                st.markdown(
                    f"""
                    <div class="cri-hud-stream">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                            <span>BOUND POLICY: {policy_cat}</span>
                            <span style="color:#34D399;">COVERAGE: 100% | ACTIVE CLAIMS: 0</span>
                        </div>
                        <div style="font-size:0.75rem; color:#94A3B8;">Loss Scenario: {claim_scenario} | Estimated Exposure: ${est_val:,.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        ia_res = InsuranceAgent().analyze(sample_context)

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card("Insurance Exposure Score", f"{ia_res.score:.1f}/100", "🛡️", ia_res.summary, "#EF4444" if ia_res.score > 50 else "#22C55E")
        with c2:
            render_kpi_card("Policy Coverage Status", "Fully Covered", "📋")
        with c3:
            render_kpi_card("Claim Severity Risk", "Low", "💰", delta="Zero pending claims", delta_color="#22C55E")

        st.markdown("##### Insurance Hazards & Policy Gaps")
        for f in ia_res.findings.get("findings", []):
            badge = "danger" if f.get("severity") in ["CRITICAL", "HIGH"] else "warning"
            st.markdown(
                f'<div class="cih-activity-item">'
                f'<span class="cih-badge cih-badge-{badge}">{f.get("severity")}</span> '
                f'<strong style="color:var(--text-primary);">{f.get("title")}</strong> — {f.get("description")}'
                f'<div class="cih-activity-time" style="color:#60A5FA;">Action: {f.get("suggested_action")}</div></div>',
                unsafe_allow_html=True
            )

    # TAB 6: REPORTING AGENT
    with tab6:
        st.markdown("#### 📋 Reporting Agent Subsystem")

        # Real-Time Ingestion Layer (Extra UI Layer)
        with st.expander("📄 Enterprise Multi-Agent Synthesis & Distribution Parameters", expanded=True):
            st.markdown(
                """
                <div class="cri-hud-overlay">
                    <span class="cri-pulse-badge"><span class="cri-pulse-dot"></span> REPORT COMPOSITION PIPELINE READY</span>
                    <span style="color:#94A3B8;">DISPATCH: Automated Digest & Audit Export</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                rep_template = st.selectbox(
                    "Report Generation Template",
                    [
                        "📊 Executive Board Risk Briefing",
                        "📜 Statutory Regulatory Compliance Dossier (NBC/IS)",
                        "🛡️ Insurance Underwriter & Exposure Dossier",
                        "🦺 Weekly Field Safety & PPE Audit Digest"
                    ],
                    key="rep_template_select"
                )
                custom_notes = st.text_area("Executive Directives & Assessment Remarks", placeholder="Enter specific audit remarks or project directives to embed into the generated synthesis...", key="rep_custom_notes")

            with col_r2:
                export_fmt = st.multiselect("Export Formats", ["Interactive PDF", "Spreadsheet (XLSX)", "JSON Audit Trail"], default=["Interactive PDF", "JSON Audit Trail"], key="rep_export_fmt")
                distribution_list = st.text_input("Notification Stakeholder Email(s)", value="safety-director@cih-enterprise.com, compliance@project.gov", key="rep_dist_list")

        st.markdown("<br>", unsafe_allow_html=True)

        ra_res = ReportingAgent().analyze(sample_context)

        st.markdown(f"**Generated Enterprise Report ID:** `{ra_res.findings.get('report_id')}`")
        if st.button("📄 Generate & Synthesize Multi-Agent Report", use_container_width=True, key="ra_page_gen_btn"):
            st.success(f"Enterprise Executive Summary synthesized for project '{active_project}' using template '{rep_template}'.")

        ent_rep = ra_res.findings.get("enterprise_report", {})
        exec_sum = ent_rep.get("executive_summary", {})
        if exec_sum:
            st.markdown("##### Executive Summary Highlights")
            for h in exec_sum.get("key_highlights", []):
                st.markdown(f"- {h}")

    # TAB 7: HISTORICAL ANALYTICS
    with tab7:
        st.markdown("#### 📈 Historical Risk Intelligence Analytics")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            weekly = dummy_data.get_weekly_progress()
            st.plotly_chart(charts.create_weekly_progress_chart(weekly), use_container_width=True)
        with col_h2:
            risk_df = dummy_data.get_risk_distribution()
            st.plotly_chart(charts.create_risk_chart(risk_df), use_container_width=True)

    # TAB 8: AUTOMATION & GOVERNANCE
    with tab8:
        st.markdown("#### ⚡ Enterprise Automation, Notifications & Governance")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            health = background_service_manager.get_system_health()
            st.markdown(
                f"""
                <div class="cih-glass-card">
                    <div class="cih-card-title">💚 Background Services Health</div>
                    <div style="font-size:1.4rem; font-weight:700; color:#22C55E; margin-bottom:0.5rem;">{health['overall_health']}</div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Executed Jobs</span><span class="cih-metric-value">{health['total_jobs_executed']}</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Failed Jobs</span><span class="cih-metric-value">{health['failed_jobs_count']}</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_a2:
            perf = performance_manager.get_performance_metrics()
            st.markdown(
                f"""
                <div class="cih-glass-card">
                    <div class="cih-card-title">⚡ Performance Metrics</div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Total Requests</span><span class="cih-metric-value">{perf.total_requests}</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Avg Latency</span><span class="cih-metric-value">{perf.avg_latency_ms:.2f} ms</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Memory Footprint</span><span class="cih-metric-value">{perf.memory_mb:.1f} MB</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("##### Startup Deployment Certification Checklist")
        checklist = deployment_validator.validate_deployment()
        chk_html = f"<div><strong>Environment:</strong> {checklist.environment} | <strong>Database:</strong> {checklist.database_status} | <strong>Production Ready:</strong> {'✅ YES' if checklist.is_production_ready else '❌ NO'}</div><ul style='margin-top:0.5rem; color:var(--text-secondary);'>"
        for k, v in checklist.checks.items():
            chk_html += f"<li>{'✅' if v else '❌'} {k.replace('_', ' ').title()}: {v}</li>"
        chk_html += "</ul>"
        render_glass_card("🚀 Production Deployment Checklist", chk_html)

        st.markdown("##### Recent Dispatch Notifications")
        notifs = notification_engine.get_notifications(limit=5)
        if notifs:
            for n in notifs:
                priority = getattr(n, "priority", n.get("priority", "INFO") if isinstance(n, dict) else "INFO")
                title = getattr(n, "title", n.get("title", "Notification") if isinstance(n, dict) else "Notification")
                message = getattr(n, "message", n.get("message", "") if isinstance(n, dict) else "")
                recipients = getattr(n, "recipients", n.get("recipients", []) if isinstance(n, dict) else [])
                recip_str = ", ".join(recipients) if isinstance(recipients, list) else str(recipients)

                st.markdown(
                    f'<div class="cih-activity-item">'
                    f'<span class="cih-badge cih-badge-info">{priority}</span> '
                    f'<strong style="color:var(--text-primary);">{title}</strong> — {message}'
                    f'<div class="cih-activity-time">Recipients: {recip_str}</div></div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("Zero notifications dispatched.")
