"""Construction Intelligence Hub - Main Application Entry Point."""

import importlib
import sys
from pathlib import Path

import streamlit as st

# Ensure project root is on path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from utils.styles import inject_global_styles, render_sidebar_branding  # noqa: E402
from utils.auth import init_auth_session, is_authenticated, render_login_page, render_logout_button  # noqa: E402
from backend.startup import initialize_hybrid_runtime  # noqa: E402

# Page configuration
st.set_page_config(
    page_title="Construction Intelligence Hub",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navigation map for high-performance lazy module loading
PAGE_MODULES = {
    "🏠 Dashboard": "modules.dashboard",
    "🛡️ Construction Risk Intelligence": "modules.construction_risk",
    "🤖 AI Analysis": "modules.ai_analysis",
    "🏗️ 3D Building Visualizer": "modules.building_visualizer",
    "📁 Project Management": "modules.project_management",
    "💰 Cost Estimation": "modules.cost_estimation",
    "🧱 Material Management": "modules.material_management",
    "👷 Worker Management": "modules.worker_management",
    "🦺 Safety Monitoring": "modules.safety_monitoring",
    "🚜 Equipment Tracking": "modules.equipment_tracking",
    "📈 Progress Monitoring": "modules.progress_monitoring",
    "📄 Reports": "modules.reports",
    "⚙ Settings": "modules.settings",
    "ℹ About": "modules.about",
}


@st.cache_resource(show_spinner=False)
def load_page_module(module_path: str):
    """Dynamically import and cache page module on demand."""
    return importlib.import_module(module_path)


@st.cache_data(ttl=60, show_spinner=False)
def _get_cached_sidebar_projects():
    from backend.services.project_service import project_service
    return project_service.get_all_projects()


def main() -> None:
    """Run the CIH application."""
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

    # Initialize authentication session state
    init_auth_session()

    # Authentication gateway check: Display login page if not authenticated
    if not is_authenticated():
        render_login_page()
        return

    startup_context = initialize_hybrid_runtime()
    if startup_context.get("startup_status") == "deferred":
        st.info("Runtime is waiting for DATABASE_URL configuration.")

    # Get selected page from session state early (defaults to first page)
    current_page = st.session_state.get("navigation_selection", "🏠 Dashboard")
    inject_global_styles(current_page)

    logo_path = ROOT / "assets" / "logo.png"

    with st.sidebar:
        render_sidebar_branding(str(logo_path) if logo_path.exists() else None)
        st.markdown("---")

        # CURRENT PROJECT Selector Control
        try:
            from backend.workflow.project_workflow import project_workflow
            
            db_projs = _get_cached_sidebar_projects()
            if db_projs:
                active_obj = project_workflow.get_active_project()
                curr_active_id = active_obj.id if active_obj else db_projs[0].id
                
                proj_map = {}
                sel_idx = 0
                for idx, p in enumerate(db_projs):
                    label = f"🏗️ {p.project_name}"
                    proj_map[label] = p
                    if p.id == curr_active_id:
                        sel_idx = idx

                def _on_sidebar_project_change():
                    new_val = st.session_state.get("sidebar_active_project_selector")
                    if new_val in proj_map:
                        project_workflow.set_active_project(proj_map[new_val].id)

                st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; margin-bottom:4px;'>CURRENT PROJECT</div>", unsafe_allow_html=True)
                
                selected_label = st.selectbox(
                    "CURRENT PROJECT",
                    list(proj_map.keys()),
                    index=sel_idx,
                    key="sidebar_active_project_selector",
                    on_change=_on_sidebar_project_change,
                    label_visibility="collapsed"
                )
                chosen_proj = proj_map.get(selected_label) or db_projs[sel_idx]
                
                # Active project metadata pill
                b_type = getattr(chosen_proj, "building_type", None) or "Commercial"
                status_txt = getattr(chosen_proj, "status", None) or "In Progress"
                st.markdown(
                    f"""
                    <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 6px; padding: 6px 10px; margin-top: 4px; margin-bottom: 4px;">
                        <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 500; display: flex; align-items: center; justify-content: space-between;">
                            <span style="color: #60A5FA; font-weight: 700;">{chosen_proj.project_code}</span>
                            <span style="color: #34D399; font-size: 0.7rem; font-weight: 600;">{status_txt}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        except Exception:
            pass

        st.markdown("---")
        selection = st.radio(
            "Navigation",
            list(PAGE_MODULES.keys()),
            label_visibility="collapsed",
            key="navigation_selection",
        )
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align:center; padding:0.5rem 0 0.75rem 0; color:#64748B; font-size:0.75rem;">
                <div style="color:#3B82F6; font-weight:600;">CIH v1.0</div>
                <div style="margin-top:0.25rem;">Enterprise Platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_logout_button()

    # Workspace Header Active Project Indicator
    try:
        from backend.workflow.project_workflow import project_workflow
        active_proj = project_workflow.get_active_project()
        if active_proj:
            st.markdown(
                f"""
                <div style="background: linear-gradient(90deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.5)); border-left: 3px solid #3B82F6; padding: 4px 12px; margin-bottom: 10px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.8rem; color: #94A3B8;">CURRENT PROJECT: <strong style="color: #F8FAFC;">{active_proj.project_name}</strong> (<span style="color: #60A5FA;">{active_proj.project_code}</span>)</span>
                    <span style="font-size: 0.72rem; color: #34D399; background: rgba(34, 197, 94, 0.1); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.3);">{active_proj.status or "IN PROGRESS"}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception:
        pass

    # Lazy-load and render selected page
    module_path = PAGE_MODULES.get(selection, "modules.dashboard")
    page_module = load_page_module(module_path)
    page_module.render()

    # Context communication bridge for floating AI Copilot
    try:
        import textwrap
        from services.ollamaService import get_module_context
        page_context = get_module_context(selection, project_id=st.session_state.get("active_project_id"))
        st.markdown(
            textwrap.dedent(
                f"""
                <div id="cih-active-context" data-module="{selection}" style="display:none;"></div>
                <textarea id="cih-active-context-data" style="display:none;">{page_context}</textarea>
                """
            ),
            unsafe_allow_html=True,
        )
    except Exception:
        # Graceful fallback to avoid interrupting rendering if context compilation fails
        st.markdown(
            f'<div id="cih-active-context" data-module="{selection}" style="display:none;"></div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
