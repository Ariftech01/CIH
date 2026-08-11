"""
Sidebar Radio Glassmorphism Injection
─────────────────────────────────────
Helper utility to inject glassmorphism CSS into your Streamlit app.
Non-destructive: Drop into app.py at the top of your code.
"""

import streamlit as st

def apply_sidebar_radio_glassmorphism():
    """
    Injects glassmorphism CSS styling for sidebar radio navigation.
    
    Features:
    - Theme-aware (auto-adapts to Streamlit light/dark toggle)
    - Modern glass morphism design with blur & transparency
    - Smooth micro-interactions (hover, active, selected states)
    - Scope-locked: ONLY affects sidebar radio elements
    - No Python structure changes required
    
    Usage:
    ------
        # At the top of app.py, after imports:
        apply_sidebar_radio_glassmorphism()
        
        # Then use st.radio as normal:
        page = st.sidebar.radio("Navigation", ["Dashboard", "Reports", "Settings"])
    """
    
    css = """
    <!-- Glassmorphism Sidebar Radio Navigation -->
    <style>
    /* SCOPE: Sidebar Radio Group Container */
    [data-testid="stSidebar"] div[role="radiogroup"] {
      gap: 0.5rem !important;
      padding: 0.5rem 0 !important;
    }
    
    /* HIDE NATIVE RADIO ARTIFACTS */
    [data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {
      display: none !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > div {
      background-color: transparent !important;
      border: none !important;
      box-shadow: none !important;
      padding: 0 !important;
      margin: 0 !important;
    }
    
    /* GLASSMORPHISM LABEL STYLING */
    /* Default (Unselected) State: clean borderless typography flush against background */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
      background: transparent !important;
      border: 1px solid transparent !important;
      border-left: 4px solid transparent !important;
      box-shadow: none !important;
      border-radius: 10px !important;
      padding: 0.75rem 1rem !important;
      margin: 0 !important;
      cursor: pointer !important;
      transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
      color: var(--text-color) !important;
    }
    
    /* Ensure label markdown/text containers remain fully visible */
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label span {
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      color: #94A3B8 !important;
      font-weight: 600 !important;
    }
    
    /* HOVER STATE: Enhanced glassmorphism */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
      background: color-mix(in srgb, var(--text-color) 6%, transparent) !important;
      border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent) !important;
      border-left: 4px solid color-mix(in srgb, var(--text-color) 10%, transparent) !important;
      transform: translateY(-1px);
    }
    
    /* SELECTED STATE: Accent highlight using primary color */
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
    [data-testid="stSidebar"] div[role="radiogroup"] div[data-checked="true"] label,
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input[type="radio"]:checked) {
      background: color-mix(in srgb, var(--primary-color) 12%, transparent) !important;
      backdrop-filter: blur(12px) !important;
      -webkit-backdrop-filter: blur(12px) !important;
      border: 1px solid var(--primary-color) !important;
      border-left: 4px solid var(--primary-color) !important;
      color: var(--primary-color) !important;
      font-weight: 700 !important;
      box-shadow: 0 4px 12px color-mix(in srgb, var(--primary-color) 15%, transparent),
                  0 0 8px color-mix(in srgb, var(--primary-color) 20%, transparent) !important;
      transform: translateY(-1px);
    }

    /* Ensure active label child elements inherit primary color */
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] *,
    [data-testid="stSidebar"] div[role="radiogroup"] div[data-checked="true"] label *,
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input[type="radio"]:checked) * {
      color: var(--primary-color) !important;
    }
    
    /* FOCUS STATE: Keyboard navigation accessibility */
    [data-testid="stSidebar"] div[role="radiogroup"] label:focus-within {
      outline: 2px solid var(--primary-color) !important;
      outline-offset: 2px !important;
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# EXAMPLE INTEGRATION (copy into your app.py)
# ───────────────────────────────────────────────────────────────
"""
import streamlit as st
from your_module import apply_sidebar_radio_glassmorphism  # Import this function

st.set_page_config(page_title="Construction Intelligence Hub", layout="wide")

# Apply glassmorphism styling (call once, near top)
apply_sidebar_radio_glassmorphism()

# Your existing routing structure - NO CHANGES NEEDED
PAGES = {
    "Dashboard": "modules.dashboard",
    "Project Management": "modules.project_management",
    "Material Management": "modules.material_management",
    "Equipment Tracking": "modules.equipment_tracking",
    "Worker Management": "modules.worker_management",
    "Safety Monitoring": "modules.safety_monitoring",
    "Progress Monitoring": "modules.progress_monitoring",
    "Cost Estimation": "modules.cost_estimation",
    "Reports": "modules.reports",
    "AI Analysis": "modules.ai_analysis",
    "Settings": "modules.settings",
    "About": "modules.about",
}

# Native st.radio - will be styled by injected CSS
page = st.sidebar.radio("Navigation", list(PAGES.keys()))

# Load selected page module as normal
if page in PAGES:
    module = __import__(PAGES[page], fromlist=[PAGES[page].split(".")[-1]])
    module.main()
"""
