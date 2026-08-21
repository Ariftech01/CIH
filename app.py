"""Agentic AI for Safety Monitoring with Construction Risk Analytics - Main Application Entry Point."""

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
    page_title="Agentic AI for Safety Monitoring with Construction Risk Analytics",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navigation map for high-performance lazy module loading
PAGE_MODULES = {
    "🏠 Dashboard": "modules.dashboard",
    "🛡️ Risk Intelligence": "modules.construction_risk",
    "🤖 AI Analysis": "modules.ai_analysis",
    "🏗️ 3D Building Visualizer": "modules.building_visualizer",
    "📁 Project Management": "modules.project_management",
    "🚧 Construction Operations": "modules.construction_operations",
    "📄 Reports": "modules.reports",
    "⚙ Settings": "modules.settings",
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
        selection = st.radio(
            "Navigation",
            list(PAGE_MODULES.keys()),
            label_visibility="collapsed",
            key="navigation_selection",
        )
        render_logout_button()

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
