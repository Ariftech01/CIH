"""Global styling and reusable UI components for CIH."""

import streamlit as st


def inject_global_styles(active_page: str = None) -> None:
    """Inject enterprise CSS theme variables and custom styles."""
    theme = st.session_state.get("theme", "Dark")
    
    if theme == "Light":
        theme_vars = """
        :root {
            --bg-gradient: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, #F8FAFC 100%);
            --sidebar-bg: rgba(241, 245, 249, 0.95);
            --sidebar-border: rgba(15, 23, 42, 0.08);
            --card-bg: rgba(255, 255, 255, 0.85);
            --card-border: rgba(15, 23, 42, 0.1);
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --text-muted: #64748B;
            --card-shadow: rgba(15, 23, 42, 0.06);
            --divider: rgba(15, 23, 42, 0.08);
            --tab-bg: rgba(15, 23, 42, 0.05);
            --tab-selected: rgba(59, 130, 246, 0.15);
            --tab-text-selected: #2563EB;
            --df-border: rgba(15, 23, 42, 0.08);
            --metric-bg: rgba(255, 255, 255, 0.85);
            --progress-bg: rgba(15, 23, 42, 0.1);
            --input-bg: rgba(255, 255, 255, 0.95);
            --input-text: #0F172A;
            --badge-border-alpha: 0.25;
            --space-xs: 8px;
            --space-sm: 12px;
            --space-md: 16px;
            --space-lg: 20px;
            --space-xl: 24px;
            --space-2xl: 32px;
            --space-3xl: 40px;
            --primary-color: #3B82F6;
            --primary-hover: #2563EB;
        }
        """
    else:
        theme_vars = """
        :root {
            --bg-gradient: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
            --sidebar-bg: rgba(15, 23, 42, 0.95);
            --sidebar-border: rgba(255, 255, 255, 0.08);
            --card-bg: rgba(255, 255, 255, 0.08);
            --card-border: rgba(255, 255, 255, 0.12);
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --card-shadow: rgba(0, 0, 0, 0.25);
            --divider: rgba(255, 255, 255, 0.08);
            --tab-bg: rgba(255, 255, 255, 0.05);
            --tab-selected: rgba(59, 130, 246, 0.25);
            --tab-text-selected: #FFFFFF;
            --df-border: rgba(255, 255, 255, 0.08);
            --metric-bg: rgba(255, 255, 255, 0.08);
            --progress-bg: rgba(255, 255, 255, 0.1);
            --input-bg: rgba(255, 255, 255, 0.05);
            --input-text: #FFFFFF;
            --badge-border-alpha: 0.4;
            --space-xs: 8px;
            --space-sm: 12px;
            --space-md: 16px;
            --space-lg: 20px;
            --space-xl: 24px;
            --space-2xl: 32px;
            --space-3xl: 40px;
            --primary-color: #3B82F6;
            --primary-hover: #2563EB;
        }
        """

    st.markdown(
        f"""
        <style>
        {theme_vars}
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }}

        .stApp {{
            background: var(--bg-gradient) !important;
            background-attachment: fixed;
        }}

        /* Style the header container: transparent background and no bottom border */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
            border-bottom: none !important;
        }}
        
        /* Hide top header decoration bar */
        [data-testid="stHeaderDecoration"] {{
            display: none !important;
        }}
        
        /* Hide Deploy button in header */
        header[data-testid="stHeader"] [data-testid="stBaseButton-header"] {{
            display: none !important;
        }}
        
        /* Hide Main Menu button in header */
        header[data-testid="stHeader"] [data-testid="stMainMenuButton"],
        #MainMenu {{
            display: none !important;
        }}
        
        /* Hide footer */
        footer {{
            display: none !important;
        }}

        section[data-testid="stSidebar"],
        [data-testid="stSidebar"] {{
            background: var(--sidebar-bg) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--sidebar-border) !important;
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            flex-basis: 300px !important;
            overflow: hidden !important;
        }}

        /* Streamlit 1.30+ Sidebar Header & Collapse Controls */
        [data-testid="stSidebarHeader"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"] {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            visibility: hidden !important;
        }}

        /* Reset outer sidebar wrapper so padding is not applied twice */
        section[data-testid="stSidebar"] > div,
        [data-testid="stSidebarContent"] {{
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
            overflow-y: hidden !important;
            overflow-x: hidden !important;
            height: 100vh !important;
            max-height: 100vh !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important;
            box-sizing: border-box !important;
        }}

        /* Dedicated single inner sidebar user content container */
        [data-testid="stSidebarUserContent"] {{
            padding-top: 40px !important;
            padding-bottom: 16px !important;
            padding-left: 16px !important;
            padding-right: 16px !important;
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
            overflow-y: hidden !important;
            overflow-x: hidden !important;
            height: 100% !important;
            max-height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important;
            box-sizing: border-box !important;
        }}

        [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"],
        [data-testid="stSidebarUserContent"] [data-testid="stVerticalBlockBorderWrapper"],
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
        section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{
            gap: 0px !important;
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
            min-height: 100% !important;
            justify-content: flex-start !important;
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
            box-sizing: border-box !important;
        }}

        [data-testid="stSidebarUserContent"] [data-testid="stElementContainer"] {{
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }}

        .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
            animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes pulseGlow {{
            0%, 100% {{ box-shadow: 0 4px 24px rgba(59, 130, 246, 0.15); }}
            50% {{ box-shadow: 0 8px 32px rgba(59, 130, 246, 0.35); }}
        }}

        @keyframes shimmer {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}

        /* WCAG 2.2 Level AA Compliant High-Contrast Focus Ring for Dark/Glass Surfaces */
        button:focus-visible,
        a:focus-visible,
        input:focus-visible,
        textarea:focus-visible,
        select:focus-visible,
        [data-baseweb="input"]:focus-within,
        [data-baseweb="select"]:focus-within,
        [data-baseweb="checkbox"]:focus-within,
        [data-baseweb="radio"]:focus-within,
        .stTabs [data-baseweb="tab-list"] button:focus-visible,
        .stButton button:focus-visible,
        .stDownloadButton button:focus-visible,
        .stFormSubmitButton button:focus-visible,
        .cih-assistant-fab:focus-visible,
        .cih-assistant-btn-control:focus-visible,
        .cih-assistant-btn-send:focus-visible,
        .cih-assistant-input:focus-visible {{
            outline: 2px solid #60A5FA !important;
            outline-offset: 2px !important;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.35) !important;
            transition: outline 0.15s ease, box-shadow 0.15s ease !important;
        }}

        .cih-page-header {{
            margin-bottom: 1.75rem;
            border-bottom: 1px solid var(--divider);
            padding-bottom: 1rem;
        }}

        .cih-page-title {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-primary) !important;
            margin: 0;
            letter-spacing: -0.025em;
            line-height: 1.2;
        }}

        .cih-page-subtitle {{
            font-size: 0.95rem;
            color: var(--text-secondary) !important;
            margin-top: 0.35rem;
            margin-bottom: 0;
            font-weight: 400;
        }}

        .cih-kpi-card {{
            background: var(--card-bg) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border) !important;
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 8px 32px var(--card-shadow) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeIn 0.4s ease-out;
            min-height: 115px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .cih-kpi-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(59, 130, 246, 0.45) !important;
            box-shadow: 0 12px 40px rgba(59, 130, 246, 0.18) !important;
        }}

        .cih-kpi-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-secondary) !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.35rem;
        }}

        .cih-kpi-value {{
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--text-primary) !important;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }}

        .cih-kpi-icon {{
            font-size: 1.5rem;
            float: right;
            opacity: 0.85;
        }}

        .cih-kpi-delta {{
            font-size: 0.8rem;
            margin-top: 0.4rem;
            font-weight: 500;
        }}

        .cih-glass-card {{
            background: var(--card-bg) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border) !important;
            border-radius: 16px;
            padding: 1.35rem;
            box-shadow: 0 8px 32px var(--card-shadow) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1.25rem;
        }}

        .cih-glass-card:hover {{
            border-color: rgba(59, 130, 246, 0.35) !important;
            box-shadow: 0 12px 40px rgba(59, 130, 246, 0.12) !important;
        }}

        .cih-card-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary) !important;
            margin-bottom: 0.85rem;
            letter-spacing: -0.01em;
        }}

        .cih-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .cih-badge-success {{ background: rgba(34, 197, 94, 0.2) !important; color: #22C55E !important; border: 1px solid rgba(34, 197, 94, var(--badge-border-alpha)) !important; }}
        .cih-badge-warning {{ background: rgba(245, 158, 11, 0.2) !important; color: #F59E0B !important; border: 1px solid rgba(245, 158, 11, var(--badge-border-alpha)) !important; }}
        .cih-badge-danger {{ background: rgba(239, 68, 68, 0.2) !important; color: #EF4444 !important; border: 1px solid rgba(239, 68, 68, var(--badge-border-alpha)) !important; }}
        .cih-badge-info {{ background: rgba(59, 130, 246, 0.2) !important; color: #3B82F6 !important; border: 1px solid rgba(59, 130, 246, var(--badge-border-alpha)) !important; }}
        .cih-badge-neutral {{ background: rgba(148, 163, 184, 0.2) !important; color: #94A3B8 !important; border: 1px solid rgba(148, 163, 184, var(--badge-border-alpha)) !important; }}

        .cih-equipment-card {{
            background: var(--card-bg) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border) !important;
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.35s ease;
            height: 100%;
        }}

        .cih-equipment-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(59, 130, 246, 0.45) !important;
            box-shadow: 0 12px 36px rgba(59, 130, 246, 0.18) !important;
        }}

        .cih-equipment-name {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary) !important;
            margin-bottom: 1rem;
        }}

        .cih-metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px solid var(--divider) !important;
            font-size: 0.85rem;
        }}

        .cih-metric-label {{ color: var(--text-secondary) !important; }}
        .cih-metric-value {{ color: var(--text-primary) !important; font-weight: 600; }}

        .cih-progress-bar {{
            background: var(--progress-bg) !important;
            border-radius: 999px;
            height: 8px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}

        .cih-progress-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #3B82F6, #60A5FA);
            transition: width 1s ease-out;
        }}

        .cih-activity-item {{
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--divider) !important;
            animation: fadeIn 0.4s ease-out;
        }}

        .cih-activity-time {{
            font-size: 0.75rem;
            color: var(--text-muted) !important;
        }}

        .cih-activity-text {{
            font-size: 0.88rem;
            color: var(--text-primary) !important;
            margin-top: 0.2rem;
        }}

        .cih-sidebar-brand {{
            text-align: center;
            padding: 0;
            margin-top: 0;
            margin-bottom: 16px;
            flex-shrink: 0;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }}

        .cih-sidebar-title {{
            font-size: 16px;
            font-weight: 800;
            line-height: 21px;
            background: linear-gradient(135deg, #3B82F6, #60A5FA);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.01em;
            text-align: center;
            white-space: normal;
            word-break: normal !important;
            overflow-wrap: break-word !important;
            word-wrap: normal !important;
            margin-top: 0;
            margin-bottom: 5px;
            padding: 0 2px;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            -webkit-box-decoration-break: clone;
            box-decoration-break: clone;
        }}

        .cih-sidebar-tagline {{
            font-size: 13.5px;
            color: var(--text-muted) !important;
            margin-top: 0;
            margin-bottom: 0;
            text-align: center;
            white-space: normal;
            line-height: 18px;
            padding: 0 2px;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }}

        .cih-report-card {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .cih-report-card:hover {{
            transform: translateY(-6px);
            border-color: #3B82F6 !important;
            box-shadow: 0 16px 48px rgba(59, 130, 246, 0.2);
        }}

        .cih-report-icon {{ font-size: 2.5rem; margin-bottom: 0.75rem; }}
        .cih-report-name {{ font-weight: 600; color: var(--text-primary) !important; font-size: 1rem; }}

        .cih-about-hero {{
            text-align: center;
            padding: 3rem 2rem;
            background: var(--card-bg) !important;
            border-radius: 24px;
            border: 1px solid var(--card-border) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }}

        .cih-skeleton {{
            background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.12) 50%, rgba(255,255,255,0.05) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 8px;
            height: 20px;
        }}

        div[data-testid="stMetric"] {{
            background: var(--card-bg) !important;
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            border: 1px solid var(--card-border) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: var(--text-primary) !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {{
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
        }}

        /* ENTERPRISE UNIFIED BUTTON SYSTEM */
        .stButton > button, .stDownloadButton > button, div[data-testid="stForm"] button[type="submit"] {{
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(59, 130, 246, 0.4) !important;
            border-radius: 10px !important;
            padding: 0.55rem 1.25rem !important;
            min-height: 42px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3) !important;
            letter-spacing: 0.01em !important;
        }}

        .stButton > button:hover, .stDownloadButton > button:hover, div[data-testid="stForm"] button[type="submit"]:hover {{
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.45) !important;
            border-color: rgba(96, 165, 250, 0.6) !important;
        }}

        .stButton > button:active, .stDownloadButton > button:active, div[data-testid="stForm"] button[type="submit"]:active {{
            transform: translateY(0) !important;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
        }}

        /* ENTERPRISE FORM CONTROLS & INPUTS */
        .stSelectbox label, .stTextInput label, .stNumberInput label,
        .stDateInput label, .stTextArea label, .stMultiSelect label,
        .stCheckbox label, .stRadio label {{
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            margin-bottom: 0.35rem !important;
            letter-spacing: 0.01em !important;
        }}

        .stTextInput input, .stNumberInput input, .stDateInput input, .stTextArea textarea,
        div[data-baseweb="select"] > div {{
            background: var(--input-bg) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 10px !important;
            color: var(--input-text) !important;
            font-size: 0.9rem !important;
            transition: all 0.2s ease !important;
        }}

        .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus, .stTextArea textarea:focus,
        div[data-baseweb="select"]:focus-within > div {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.35) !important;
        }}

        /* ENTERPRISE DATAFRAME & TABLE STANDARDIZATION */
        div[data-testid="stDataFrame"] {{
            border-radius: 14px !important;
            overflow: hidden !important;
            border: 1px solid var(--df-border) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
            background: var(--card-bg) !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: var(--tab-bg) !important;
            border-radius: 12px;
            padding: 5px;
            border: 1px solid var(--card-border) !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            color: var(--text-secondary) !important;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
        }}

        .stTabs [aria-selected="true"] {{
            background: var(--tab-selected) !important;
            color: var(--tab-text-selected) !important;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
        }}

        hr {{
            border: 0 !important;
            border-top: 1px solid var(--divider) !important;
            margin: 1.5rem 0 !important;
        }}

        /* Ensure normal markdown paragraphs and headers adapt */
        .stApp [data-testid="stMarkdownContainer"] p, 
        .stApp [data-testid="stMarkdownContainer"] h1, 
        .stApp [data-testid="stMarkdownContainer"] h2, 
        .stApp [data-testid="stMarkdownContainer"] h3, 
        .stApp [data-testid="stMarkdownContainer"] h4, 
        .stApp [data-testid="stMarkdownContainer"] h5, 
        .stApp [data-testid="stMarkdownContainer"] h6,
        .stApp [data-testid="stMarkdownContainer"] li {{
            color: var(--text-primary) !important;
        }}

        /* Theme awareness for input text fields and selects */
        .stApp input, .stApp select, .stApp textarea, .stApp div[role="combobox"] {{
            color: var(--input-text) !important;
        }}

        /* ─────────────────────────────────────────────────────────── */
        /* GLASSMORPHISM SIDEBAR RADIO NAVIGATION & LOGOUT */
        /* ─────────────────────────────────────────────────────────── */
        
        [data-testid="stSidebar"] div[data-testid="stRadio"] {{
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }}

        /* Container styling */
        [data-testid="stSidebar"] div[role="radiogroup"] {{
            gap: 5px !important;
            padding: 0 !important;
            margin: 0 !important;
            flex-shrink: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            box-sizing: border-box !important;
        }}

        /* Hide native radio input element and radio circle visual */
        [data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"],
        [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child:not([data-testid="stMarkdownContainer"]) {{
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        /* Remove default Streamlit list margins/borders/backgrounds from container wrapper */
        [data-testid="stSidebar"] div[role="radiogroup"] > div {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }}

        /* Default (Unselected) state for option labels */
        [data-testid="stSidebar"] div[role="radiogroup"] label {{
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            border-left: 3px solid transparent !important;
            box-shadow: none !important;
            border-radius: 8px !important;
            padding: 0 12px !important;
            margin: 0 !important;
            min-height: 42px !important;
            height: 42px !important;
            max-height: 42px !important;
            width: 100% !important;
            max-width: 100% !important;
            cursor: pointer !important;
            transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            white-space: nowrap !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }}

        /* Ensure label text and markdown containers remain fully visible and on a SINGLE LINE */
        [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] div[role="radiogroup"] label p,
        [data-testid="stSidebar"] div[role="radiogroup"] label span {{
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            visibility: visible !important;
            opacity: 1 !important;
            color: var(--text-secondary) !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            margin: 0 !important;
            padding: 0 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            line-height: 1 !important;
            width: 100% !important;
        }}

        /* Hover state for unselected option labels */
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
            background: rgba(59, 130, 246, 0.08) !important;
            border: 1px solid rgba(59, 130, 246, 0.15) !important;
            border-left: 3px solid rgba(59, 130, 246, 0.5) !important;
            color: var(--text-primary) !important;
            transform: translateY(-1px);
        }}

        [data-testid="stSidebar"] div[role="radiogroup"] label:hover div[data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover p,
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover span {{
            color: var(--text-primary) !important;
        }}

        /* Active (Selected) state styling */
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
        [data-testid="stSidebar"] div[role="radiogroup"] div[data-checked="true"] label,
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input[type="radio"]:checked) {{
            background: rgba(59, 130, 246, 0.18) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(59, 130, 246, 0.4) !important;
            border-left: 3px solid #3B82F6 !important;
            color: var(--tab-text-selected, #FFFFFF) !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.25) !important;
            transform: translateY(-1px);
        }}

        /* Ensure active label child elements inherit proper active color */
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] *,
        [data-testid="stSidebar"] div[role="radiogroup"] div[data-checked="true"] label *,
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input[type="radio"]:checked) * {{
            color: var(--tab-text-selected, #FFFFFF) !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            white-space: nowrap !important;
        }}

        /* Focus state accessibility */
        [data-testid="stSidebar"] div[role="radiogroup"] label:focus-within {{
            outline: 2px solid var(--primary-color) !important;
            outline-offset: 2px !important;
        }}

        /* SIDEBAR COMPACT LOGOUT BUTTON */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has(div.stButton),
        [data-testid="stSidebar"] div:has(> div.stButton),
        [data-testid="stSidebar"] div.stButton {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin-top: auto !important;
            padding-top: 12px !important;
            margin-bottom: 0 !important;
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            flex-shrink: 0 !important;
        }}

        [data-testid="stSidebar"] div.stButton > button {{
            background: rgba(239, 68, 68, 0.1) !important;
            color: #EF4444 !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            height: 40px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            width: 235px !important;
            max-width: 235px !important;
            margin: 0 auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
            box-sizing: border-box !important;
        }}

        [data-testid="stSidebar"] div.stButton > button:hover {{
            background: rgba(239, 68, 68, 0.2) !important;
            border-color: rgba(239, 68, 68, 0.6) !important;
            color: #F87171 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
        }}

        [data-testid="stSidebar"] div.stButton > button:active {{
            transform: translateY(0) !important;
        }}

        [data-testid="stSidebar"] div.stButton > button p,
        [data-testid="stSidebar"] div.stButton > button span {{
            color: #EF4444 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin: 0 !important;
        }}

        [data-testid="stSidebar"] div.stButton > button:hover p,
        [data-testid="stSidebar"] div.stButton > button:hover span {{
            color: #F87171 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "\n".join(line.strip() for line in """
        <style>
        /* ─────────────────────────────────────────────────────────── */
        /* ENTERPRISE AI WORKSPACE & PREDICTIVE INTELLIGENCE STYLES */
        /* ─────────────────────────────────────────────────────────── */
        
        .cih-ai-workspace {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            animation: fadeIn 0.6s ease-out;
        }

        .cih-ai-status-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%) !important;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }

        .cih-ai-status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 0.75rem;
            margin-bottom: 0.75rem;
        }

        .cih-ai-status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 0.75rem;
        }

        .cih-ai-status-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 10px;
            padding: 0.5rem 0.75rem;
            font-size: 0.78rem;
        }

        .cih-ai-status-label {
            color: var(--text-secondary);
            font-weight: 500;
            margin-bottom: 0.2rem;
        }

        .cih-ai-status-value {
            font-weight: 600;
            color: var(--text-primary);
        }

        .cih-status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        .cih-status-dot.green { background-color: #22C55E; box-shadow: 0 0 8px #22C55E; }
        .cih-status-dot.red { background-color: #EF4444; box-shadow: 0 0 8px #EF4444; }
        .cih-status-dot.amber { background-color: #F59E0B; box-shadow: 0 0 8px #F59E0B; }

        .cih-predictive-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.25rem;
            margin-top: 0.5rem;
        }

        .cih-prediction-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 190px;
        }

        .cih-prediction-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
            opacity: 0;
            transition: opacity 0.4s ease;
            pointer-events: none;
        }

        .cih-prediction-card:hover {
            transform: translateY(-5px);
            border-color: rgba(59, 130, 246, 0.3) !important;
            box-shadow: 0 15px 35px rgba(59, 130, 246, 0.15);
        }

        .cih-prediction-card:hover::before {
            opacity: 1;
        }

        .cih-prediction-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .cih-prediction-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .cih-prediction-icon {
            font-size: 1.5rem;
            padding: 0.5rem;
            background: rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .cih-prediction-content {
            flex-grow: 1;
            margin-bottom: 1.25rem;
        }

        .cih-prediction-metrics {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.82rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }

        .cih-prediction-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }

        .cih-confidence-dial {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.2rem 0.5rem;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        </style>
        """.split("\n")),
        unsafe_allow_html=True,
    )

    import streamlit.components.v1 as components
    if active_page and ("AI Analysis" in active_page or "Visualizer" in active_page or "3D Building" in active_page):
        components.html(
            r"""
            <script>
            (function() {
                const hostDoc = window.parent.document || document;
                const rootNode = hostDoc.getElementById("cih-assistant-root");
                if (rootNode) {
                    rootNode.remove();
                }
                const markEl = hostDoc.getElementById("cih-assistant-script-loaded");
                if (markEl) {
                    markEl.remove();
                }
                const styleEl = hostDoc.getElementById("cih-assistant-injected-styles");
                if (styleEl) {
                    styleEl.remove();
                }
            })();
            </script>
            """,
            height=0,
            width=0,
        )
        return

    components.html(
        r"""
        <script>
        (function() {
            const hostDoc = window.parent.document || document;
            
            // 1. Prevent duplicate injector scripts
            if (hostDoc.getElementById("cih-assistant-script-loaded")) {
                return;
            }
            
            // Mark as loaded
            const markEl = hostDoc.createElement("div");
            markEl.id = "cih-assistant-script-loaded";
            markEl.style.display = "none";
            hostDoc.body.appendChild(markEl);

            // 2. Inject floating widget styles into host document head
            const styleEl = hostDoc.createElement("style");
            styleEl.id = "cih-assistant-injected-styles";
            styleEl.textContent = `
                :root {
                    --cih-primary: #3B82F6;
                    --cih-secondary: #8B5CF6;
                    --cih-accent-gradient: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
                    --cih-glass-bg: rgba(15, 23, 42, 0.85);
                    --cih-glass-border: rgba(255, 255, 255, 0.1);
                    --cih-text-primary: #F8FAFC;
                    --cih-text-secondary: #94A3B8;
                    --cih-text-muted: #64748B;
                }
                
                body.light-theme-override {
                    --cih-glass-bg: rgba(255, 255, 255, 0.92);
                    --cih-glass-border: rgba(15, 23, 42, 0.12);
                    --cih-text-primary: #0F172A;
                    --cih-text-secondary: #475569;
                    --cih-text-muted: #64748B;
                }

                #cih-assistant-root {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    z-index: 999999;
                    font-family: 'Inter', system-ui, sans-serif;
                    transition: bottom 0.3s cubic-bezier(0.16, 1, 0.3, 1), right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                }

                .cih-assistant-fab:focus-visible,
                .cih-assistant-btn-control:focus-visible,
                .cih-assistant-btn-send:focus-visible,
                .cih-assistant-input:focus-visible {
                    outline: 2px solid #3B82F6 !important;
                    outline-offset: 2px !important;
                }

                @media (max-width: 1366px) or (max-height: 800px) {
                    #cih-assistant-root {
                        bottom: 18px;
                        right: 18px;
                    }
                    .cih-assistant-fab {
                        width: 48px;
                        height: 48px;
                    }
                    .cih-assistant-fab-icon {
                        font-size: 20px;
                    }
                    .cih-assistant-window {
                        width: min(350px, calc(100vw - 32px));
                        height: min(460px, calc(100vh - 100px));
                        bottom: 74px;
                        right: 18px;
                    }
                }

                @media (max-width: 768px) {
                    #cih-assistant-root {
                        bottom: 12px;
                        right: 12px;
                    }
                    .cih-assistant-fab {
                        width: 42px;
                        height: 42px;
                    }
                    .cih-assistant-fab-icon {
                        font-size: 18px;
                    }
                    .cih-assistant-window {
                        width: calc(100vw - 24px);
                        height: calc(100vh - 110px);
                        bottom: 60px;
                        right: 12px;
                        border-radius: 14px;
                    }
                }

                .cih-assistant-fab {
                    width: 56px;
                    height: 56px;
                    border-radius: 50%;
                    background: var(--cih-accent-gradient);
                    border: none;
                    outline: none;
                    cursor: pointer;
                    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }

                .cih-assistant-fab:hover {
                    transform: scale(1.1) rotate(5deg);
                    box-shadow: 0 12px 32px rgba(139, 92, 246, 0.5);
                }

                .cih-assistant-fab-icon {
                    font-size: 24px;
                    z-index: 2;
                }

                .cih-assistant-pulse {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    background: var(--cih-primary);
                    opacity: 0.3;
                    animation: cihBreathing 2.5s infinite;
                    z-index: 1;
                }

                @keyframes cihBreathing {
                    0% { transform: scale(1); opacity: 0.35; }
                    50% { transform: scale(1.3); opacity: 0; }
                    100% { transform: scale(1); opacity: 0.35; }
                }

                .cih-assistant-window {
                    position: fixed;
                    bottom: 92px;
                    right: 24px;
                    width: 380px;
                    height: 520px;
                    background: var(--cih-glass-bg);
                    backdrop-filter: blur(24px) saturate(190%);
                    -webkit-backdrop-filter: blur(24px) saturate(190%);
                    border: 1px solid var(--cih-glass-border);
                    border-radius: 20px;
                    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
                    transform-origin: bottom right;
                    resize: both;
                    min-width: 320px;
                    min-height: 400px;
                    max-width: 600px;
                    max-height: 800px;
                }
                
                .cih-assistant-window.minimized {
                    opacity: 0;
                    transform: scale(0.6) translateY(40px);
                    pointer-events: none;
                }

                .cih-assistant-header {
                    padding: 1rem;
                    background: rgba(255, 255, 255, 0.02);
                    border-bottom: 1px solid var(--cih-glass-border);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: move;
                    user-select: none;
                }

                .cih-assistant-header-title {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    color: var(--cih-text-primary);
                }

                .cih-assistant-badge {
                    font-size: 0.7rem;
                    font-weight: 600;
                    padding: 0.2rem 0.5rem;
                    border-radius: 6px;
                    background: rgba(59, 130, 246, 0.15);
                    border: 1px solid rgba(59, 130, 246, 0.3);
                    color: #60A5FA;
                    text-transform: uppercase;
                    letter-spacing: 0.02em;
                    max-width: 140px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }

                .cih-assistant-header-controls {
                    display: flex;
                    gap: 8px;
                }

                .cih-assistant-btn-control {
                    background: transparent;
                    border: none;
                    color: var(--cih-text-secondary);
                    cursor: pointer;
                    padding: 2px;
                    font-size: 14px;
                    transition: color 0.2s;
                }

                .cih-assistant-btn-control:hover {
                    color: var(--cih-text-primary);
                }

                .cih-assistant-body {
                    flex-grow: 1;
                    padding: 1rem;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                }

                .cih-chat-msg {
                    display: flex;
                    flex-direction: column;
                    max-width: 85%;
                    animation: cihFadeIn 0.3s ease-out forwards;
                }

                .cih-chat-msg.user {
                    align-self: flex-end;
                }

                .cih-chat-msg.assistant {
                    align-self: flex-start;
                }

                .cih-chat-bubble {
                    padding: 0.75rem 1rem;
                    border-radius: 16px;
                    font-size: 0.88rem;
                    line-height: 1.4;
                    word-break: break-word;
                }
                
                .cih-chat-msg.user .cih-chat-bubble {
                    background: var(--cih-primary);
                    color: #FFFFFF;
                    border-bottom-right-radius: 4px;
                }

                .cih-chat-msg.assistant .cih-chat-bubble {
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid var(--cih-glass-border);
                    color: var(--cih-text-primary);
                    border-bottom-left-radius: 4px;
                }
                
                .cih-chat-bubble p { margin: 0 0 0.5rem 0; }
                .cih-chat-bubble p:last-child { margin-bottom: 0; }
                .cih-chat-bubble ul, .cih-chat-bubble ol { margin: 0.25rem 0; padding-left: 1.25rem; }
                .cih-chat-bubble li { margin-bottom: 2px; }
                .cih-chat-bubble table { border-collapse: collapse; width: 100%; margin: 0.5rem 0; font-size: 0.8rem; }
                .cih-chat-bubble th, .cih-chat-bubble td { border: 1px solid var(--cih-glass-border); padding: 4px 8px; text-align: left; }
                .cih-chat-bubble th { background: rgba(255,255,255,0.03); }

                .cih-chat-meta {
                    font-size: 0.7rem;
                    color: var(--cih-text-muted);
                    margin-top: 4px;
                    align-self: flex-end;
                }

                .cih-chat-msg.assistant .cih-chat-meta {
                    align-self: flex-start;
                }

                .cih-typing-indicator {
                    display: flex;
                    gap: 4px;
                    padding: 8px 16px;
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid var(--cih-glass-border);
                    border-radius: 12px;
                    align-self: flex-start;
                    width: fit-content;
                }

                .cih-typing-indicator span {
                    width: 6px;
                    height: 6px;
                    background-color: var(--cih-text-secondary);
                    border-radius: 50%;
                    animation: cihBounce 1.4s infinite ease-in-out both;
                }

                .cih-typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
                .cih-typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

                @keyframes cihBounce {
                    0%, 80%, 100% { transform: scale(0); }
                    40% { transform: scale(1); }
                }

                @keyframes cihFadeIn {
                    from { opacity: 0; transform: translateY(8px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                .cih-assistant-quick-actions {
                    padding: 0.5rem 1rem;
                    display: flex;
                    gap: 8px;
                    overflow-x: auto;
                    white-space: nowrap;
                    scrollbar-width: none;
                }
                .cih-assistant-quick-actions::-webkit-scrollbar {
                    display: none;
                }

                .cih-quick-chip {
                    font-size: 0.78rem;
                    padding: 0.4rem 0.75rem;
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid var(--cih-glass-border);
                    border-radius: 20px;
                    color: var(--cih-text-secondary);
                    cursor: pointer;
                    transition: all 0.2s;
                }

                .cih-quick-chip:hover {
                    background: rgba(59, 130, 246, 0.1);
                    border-color: var(--cih-primary);
                    color: var(--cih-text-primary);
                }

                .cih-assistant-footer {
                    padding: 1rem;
                    border-top: 1px solid var(--cih-glass-border);
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    background: rgba(255, 255, 255, 0.01);
                }

                .cih-assistant-input-wrapper {
                    display: flex;
                    gap: 8px;
                    background: rgba(255, 255, 255, 0.04);
                    border: 1px solid var(--cih-glass-border);
                    border-radius: 12px;
                    padding: 6px 12px;
                    align-items: center;
                }

                .cih-assistant-input {
                    flex-grow: 1;
                    background: transparent;
                    border: none;
                    outline: none;
                    color: var(--cih-text-primary);
                    font-size: 0.85rem;
                    resize: none;
                    max-height: 60px;
                    font-family: inherit;
                    padding: 4px 0;
                }

                .cih-assistant-input::placeholder {
                    color: var(--cih-text-muted);
                }

                .cih-assistant-btn-send {
                    background: transparent;
                    border: none;
                    color: var(--cih-primary);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 4px;
                    transition: color 0.2s, transform 0.2s;
                }

                .cih-assistant-btn-send:hover {
                    color: var(--cih-secondary);
                    transform: translate(1px, -1px);
                }
                
                .cih-assistant-btn-send.disabled {
                    color: var(--cih-text-muted) !important;
                    cursor: not-allowed;
                }

                .cih-assistant-footer-meta {
                    display: flex;
                    justify-content: space-between;
                    font-size: 0.72rem;
                    color: var(--cih-text-muted);
                    padding: 0 4px;
                }

                .cih-assistant-meta-action {
                    color: var(--cih-text-secondary);
                    text-decoration: none;
                    cursor: pointer;
                    transition: color 0.2s;
                }

                .cih-assistant-meta-action:hover {
                    color: var(--cih-primary);
                }
                
                .cih-assistant-body::-webkit-scrollbar {
                    width: 4px;
                }
                .cih-assistant-body::-webkit-scrollbar-track {
                    background: transparent;
                }
                .cih-assistant-body::-webkit-scrollbar-thumb {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 99px;
                }
                
                .cih-assistant-resize-handle {
                    position: absolute;
                    bottom: 0;
                    right: 0;
                    width: 14px;
                    height: 14px;
                    cursor: se-resize;
                    z-index: 10;
                }
                
                .cih-connection-badge {
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                    display: inline-block;
                }
                .cih-connection-badge.online { background-color: #22C55E; box-shadow: 0 0 6px #22C55E; }
                .cih-connection-badge.offline { background-color: #EF4444; box-shadow: 0 0 6px #EF4444; }
            `;
            hostDoc.head.appendChild(styleEl);

            // 3. Inject Assistant Root Node into host document body
            const rootNode = hostDoc.createElement("div");
            rootNode.id = "cih-assistant-root";
            rootNode.innerHTML = `
                <button class="cih-assistant-fab" id="cih-assistant-fab" title="Construction AI Assistant (CHIA)" aria-label="Toggle Construction AI Assistant" aria-expanded="false" tabindex="0">
                    <span class="cih-assistant-fab-icon">🤖</span>
                    <div class="cih-assistant-pulse"></div>
                </button>
                
                <div class="cih-assistant-window minimized" id="cih-assistant-window" role="region" aria-label="CIH AI Assistant Chat Window">
                    <div class="cih-assistant-header" id="cih-assistant-header">
                        <div class="cih-assistant-header-title">
                            <span class="cih-connection-badge online" id="cih-assistant-status" title="Local Ollama: Connected"></span>
                            <span style="font-weight: 700; font-size: 0.92rem;">CIH Copilot</span>
                            <span class="cih-assistant-badge" id="cih-assistant-badge">Dashboard</span>
                        </div>
                        <div class="cih-assistant-header-controls">
                            <button class="cih-assistant-btn-control" id="cih-assistant-btn-pin" title="Toggle Pinned Mode">📌</button>
                            <button class="cih-assistant-btn-control" id="cih-assistant-btn-close" title="Minimize">✖</button>
                        </div>
                    </div>
                    
                    <div class="cih-assistant-body" id="cih-assistant-body">
                        <div class="cih-chat-messages" id="cih-chat-messages"></div>
                        <div class="cih-typing-indicator" id="cih-typing-indicator" style="display: none;">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                    
                    <div class="cih-assistant-quick-actions" id="cih-assistant-quick-actions"></div>

                    <div class="cih-assistant-footer">
                        <div class="cih-assistant-input-wrapper">
                            <textarea class="cih-assistant-input" id="cih-assistant-input" placeholder="Ask construction AI..." rows="1"></textarea>
                            <button class="cih-assistant-btn-send" id="cih-assistant-btn-send" title="Send message">
                                <svg viewBox="0 0 24 24" width="18" height="18"><path fill="currentColor" d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/></svg>
                            </button>
                        </div>
                        <div class="cih-assistant-footer-meta">
                            <span id="cih-assistant-meta-time" style="font-size:0.68rem; opacity:0.8;"></span>
                            <div>
                                <a id="cih-assistant-stop-generation" class="cih-assistant-meta-action" style="display:none; color:#EF4444; margin-right:12px; font-weight:600;">Stop</a>
                                <a id="cih-assistant-clear-chat" class="cih-assistant-meta-action">Clear Chat</a>
                            </div>
                        </div>
                    </div>
                    <div class="cih-assistant-resize-handle"></div>
                </div>
            `;
            hostDoc.body.appendChild(rootNode);

            // Fetch elements from parent document
            const fab = hostDoc.getElementById("cih-assistant-fab");
            const win = hostDoc.getElementById("cih-assistant-window");
            const closeBtn = hostDoc.getElementById("cih-assistant-btn-close");
            const pinBtn = hostDoc.getElementById("cih-assistant-btn-pin");
            const header = hostDoc.getElementById("cih-assistant-header");
            const messagesContainer = hostDoc.getElementById("cih-chat-messages");
            const inputField = hostDoc.getElementById("cih-assistant-input");
            const sendBtn = hostDoc.getElementById("cih-assistant-btn-send");
            const typingIndicator = hostDoc.getElementById("cih-typing-indicator");
            const quickActionsContainer = hostDoc.getElementById("cih-assistant-quick-actions");
            const statusIndicator = hostDoc.getElementById("cih-assistant-status");
            const clearChatBtn = hostDoc.getElementById("cih-assistant-clear-chat");
            const stopBtn = hostDoc.getElementById("cih-assistant-stop-generation");
            const moduleBadge = hostDoc.getElementById("cih-assistant-badge");
            const metaTime = hostDoc.getElementById("cih-assistant-meta-time");

            // State variables
            let chatHistory = [];
            let isPinned = false;
            let activeModule = "Dashboard";
            let activeContext = "Dashboard operational data synchronized.";
            let activeController = null;
            let ollamaStatus = "connected";

            const syncTheme = () => {
                const isLight = hostDoc.body.classList.contains("light-theme-override") || 
                                (window.parent.document && window.parent.document.body.getAttribute("data-theme") === "light");
                if (isLight) {
                    hostDoc.body.classList.add("light-theme-override");
                } else {
                    hostDoc.body.classList.remove("light-theme-override");
                }
            };
            syncTheme();

            const checkOllamaHealth = async () => {
                try {
                    const start = Date.now();
                    const res = await fetch("http://127.0.0.1:11434/api/tags");
                    if (res.status === 200) {
                        const data = await res.json();
                        const latency = Date.now() - start;
                        const models = data.models || [];
                        const hasModel = models.some(m => m.name.toLowerCase().includes("llama3.2"));
                        if (hasModel) {
                            ollamaStatus = "connected";
                            statusIndicator.className = "cih-connection-badge online";
                            statusIndicator.title = `Ollama: Connected (Latency: ${latency}ms, model: llama3.2)`;
                        } else {
                            ollamaStatus = "missing";
                            statusIndicator.className = "cih-connection-badge offline";
                            statusIndicator.title = "Ollama: Connected, but llama3.2 is missing!";
                        }
                    }
                } catch(e) {
                    ollamaStatus = "offline";
                    statusIndicator.className = "cih-connection-badge offline";
                    statusIndicator.title = "Ollama: Offline. Using local simulation.";
                }
            };
            checkOllamaHealth();
            setInterval(checkOllamaHealth, 15000);

            // Suggested prompt mapping by active module
            const promptSuggestions = {
                "Dashboard": [
                    { label: "📋 Today's Summary", query: "Summarize today's overall activity and operations in CIH." },
                    { label: "⚠️ Active Risks", query: "What are the most active timeline or safety risks across projects?" },
                    { label: "💰 Cost Status", query: "Show budget utilization summary." }
                ],
                "Project Management": [
                    { label: "📁 Active Milestones", query: "Summarize the active projects on record and their progress." },
                    { label: "👤 Project Managers", query: "Who is managing the active projects, and how are they progressing?" },
                    { label: "🚨 Delayed Projects", query: "Show active projects with Delayed status and why." }
                ],
                "Material Management": [
                    { label: "🧱 Inventory Shortages", query: "Show me today's material inventory issues and low stock items." },
                    { label: "💰 Procure Costs", query: "Recommend procurement cost savings for our active materials." },
                    { label: "🚛 JIT Ready-Mix", query: "Suggest optimizations for Ready Mix Concrete (RMC) logistics." }
                ],
                "Worker Management": [
                    { label: "👷 Attendance Check", query: "How is the worker attendance today, and who is on leave?" },
                    { label: "📈 Productivity Audit", query: "How can we improve workforce productivity rating and experience ratios?" },
                    { label: "🦺 Certification Risks", query: "Suggest safety certification checks for mason and welder crews." }
                ],
                "Safety Monitoring": [
                    { label: "🦺 Incident Summary", query: "Summarize today's site safety incident log and severity levels." },
                    { label: "🚨 Compliance Checklist", query: "Show safety compliance checklist issues and mitigation recommendations." },
                    { label: "🌧️ Weather Precautions", query: "What precautions should be taken for scaffolding and crane operations under wind?" }
                ],
                "Equipment Tracking": [
                    { label: "🚜 Health Indicators", query: "Report machinery health index and list units needing scheduled maintenance." },
                    { label: "⛽ Fuel & Usage", query: "Show fuel levels and utilization hours of our fleet." },
                    { label: "🔧 Service Overdue", query: "List equipment with overdue service schedules." }
                ],
                "Cost Estimation": [
                    { label: "💰 Budget Allocations", query: "Show standard budget cost allocation categories." },
                    { label: "⚖️ Savings Options", query: "Recommend budget optimization methods based on active budgets." },
                    { label: "💸 Excess Overhead", query: "Identify fields with potential overtime or procurement excess cost." }
                ],
                "Progress Monitoring": [
                    { label: "📈 Delay Deviations", query: "Predict timeline delay risks for active milestones." },
                    { label: "🏁 Foundation Status", query: "Show progress on Foundation and Structural Frame milestones." },
                    { label: "📦 Lead-Time Impact", query: "Explain supply chain transit lead-time delays." }
                ],
                "Reports": [
                    { label: "📄 Site Report", query: "Generate today's construction site operational report." },
                    { label: "📅 Weekly Summary", query: "Compile a weekly construction progress summary report." }
                ]
            };

            const renderChips = (moduleName) => {
                quickActionsContainer.innerHTML = "";
                const cleanName = moduleName.replace(/[^a-zA-Z ]/g, "").trim();
                let chips = promptSuggestions[cleanName] || promptSuggestions["Dashboard"];
                
                chips.forEach(c => {
                    const chip = hostDoc.createElement("div");
                    chip.className = "cih-quick-chip";
                    chip.textContent = c.label;
                    chip.onclick = () => {
                        inputField.value = c.query;
                        submitChatQuery();
                    };
                    quickActionsContainer.appendChild(chip);
                });
            };

            const parseBasicMarkdown = (text) => {
                if (!text) return "";
                let html = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
                html = html.replace(/^### (.*$)/gim, '<h4 style="margin:8px 0; font-weight:600;">$1</h4>');
                html = html.replace(/^## (.*$)/gim, '<h3 style="margin:10px 0; font-weight:700;">$1</h3>');
                html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                html = html.replace(/`(.*?)`/g, '<code style="background:rgba(255,255,255,0.08); padding:1px 4px; border-radius:4px; font-family:monospace;">$1</code>');
                html = html.replace(/^\s*-\s+(.*$)/gim, '<li style="margin-left: 12px;">$1</li>');
                
                const paragraphs = html.split("\n");
                let parsedHtml = "";
                let inList = false;
                
                paragraphs.forEach(p => {
                    if (p.trim().startsWith("<li")) {
                        if (!inList) {
                            parsedHtml += '<ul style="margin: 4px 0; padding-left: 12px;">';
                            inList = true;
                        }
                        parsedHtml += p;
                    } else {
                        if (inList) {
                            parsedHtml += '</ul>';
                            inList = false;
                        }
                        if (p.trim()) {
                            parsedHtml += `<p style="margin: 0 0 6px 0;">${p}</p>`;
                        } else {
                            parsedHtml += '<div style="height: 6px;"></div>';
                        }
                    }
                });
                if (inList) parsedHtml += '</ul>';
                return parsedHtml;
            };

            const appendMessageUI = (role, text, timeStr) => {
                const msgWrapper = hostDoc.createElement("div");
                msgWrapper.className = `cih-chat-msg ${role}`;
                
                const bubble = hostDoc.createElement("div");
                bubble.className = "cih-chat-bubble";
                bubble.innerHTML = parseBasicMarkdown(text);
                
                const meta = hostDoc.createElement("div");
                meta.className = "cih-chat-meta";
                meta.textContent = timeStr || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                msgWrapper.appendChild(bubble);
                msgWrapper.appendChild(meta);
                messagesContainer.appendChild(msgWrapper);
                return bubble;
            };

            const scrollToBottom = () => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            };

            const loadHistory = () => {
                const stored = localStorage.getItem("cih_floating_chat_history");
                if (stored) {
                    chatHistory = JSON.parse(stored);
                } else {
                    chatHistory = [{
                        role: "assistant",
                        content: `Welcome to CIH Copilot. I am your specialized Construction Intelligence Advisor. I have auto-synchronized with the active **${activeModule}** context. How can I help you today?`,
                        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    }];
                    localStorage.setItem("cih_floating_chat_history", JSON.stringify(chatHistory));
                }
                renderMessages();
            };

            const renderMessages = () => {
                messagesContainer.innerHTML = "";
                chatHistory.forEach(msg => {
                    appendMessageUI(msg.role, msg.content, msg.timestamp);
                });
                scrollToBottom();
            };

            const saveAssistantMessage = (content) => {
                chatHistory.push({
                    role: "assistant",
                    content: content,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                });
                localStorage.setItem("cih_floating_chat_history", JSON.stringify(chatHistory));
                stopBtn.style.display = "none";
                sendBtn.className = "cih-assistant-btn-send";
                activeController = null;
                scrollToBottom();
            };

            const getJSMockResponse = (msg, module) => {
                const cleanMsg = msg.toLowerCase();
                const mName = module.replace(/[^a-zA-Z ]/g, "").trim().toLowerCase();
                let rep = "\n\n🤖 **[Offline Simulation] CIH Advisor:**\n";
                if (mName.includes("material")) {
                    rep += "Based on Material Management records: Tata Steel Rebar is currently at Low Stock (1100 available vs 1200 required). Ready Mix Concrete is also showing low levels due to highway delays. We recommend procuring 20 tons from Sand Corp to hedge pricing jumps expected next week.";
                } else if (mName.includes("worker") || cleanMsg.includes("attendance")) {
                    rep += "Workforce Audit: Today's attendance is at 88%. Electrical department leads at 96% compliance, while Civil labor shows high fatigue indices. Suggest implementing staggered shift rotations to improve civil crew health and avoid weekend overtime premiums (+14% cost overhead).";
                } else if (mName.includes("safety") || cleanMsg.includes("risk")) {
                    rep += "Safety Diagnostics: Current risk index is at 14.2%. However, there's a soil sliding risk in Basement grid B-4 due to high excavation moisture. Ensure Dr. Fixit waterproofing membrane is deployed and PPE compliance checks are run for crane crews.";
                } else if (mName.includes("cost") || cleanMsg.includes("budget")) {
                    rep += "Procurement & Cost Estimator: Tata Steel procured pricing index is projected to corrected by 4.2% in 6 days. Delaying current structural tower bulk purchase orders will yield an estimated ₹85,000 in immediate procurement savings.";
                } else if (cleanMsg.includes("summary") || mName.includes("dashboard")) {
                    rep += "Operational Dashboard Overview: Average progress completion is 91.2% across 25 active projects. Safety compliance score remains stable at 92.5%. Critical alert: River Sand inventory is currently flagged under Low Stock guidelines.";
                } else {
                    rep += `I've analyzed your question regarding "${msg}" in relation to the active module context. I recommend scheduling a structural review of materials ledgers, safety checklists, and project milestones to audit resource utilization. Let me know if you need specific breakdowns!`;
                }
                return rep;
            };

            const submitChatQuery = async () => {
                const text = inputField.value.trim();
                if (!text) return;
                if (typingIndicator.style.display !== "none") return;

                inputField.value = "";
                inputField.style.height = "auto";
                const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                const userMsg = { role: "user", content: text, timestamp: timeStr };
                chatHistory.push(userMsg);
                localStorage.setItem("cih_floating_chat_history", JSON.stringify(chatHistory));
                appendMessageUI("user", text, timeStr);
                scrollToBottom();

                typingIndicator.style.display = "flex";
                stopBtn.style.display = "inline";
                sendBtn.className = "cih-assistant-btn-send disabled";
                scrollToBottom();

                activeController = new AbortController();
                const startResponseTime = Date.now();
                const responseBubble = appendMessageUI("assistant", "", "");
                let assistantResponse = "";

                try {
                    // Route via Unified CIH Enterprise AI Gateway (port 8502)
                    const apiRes = await fetch("http://127.0.0.1:8502/api/chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            message: text,
                            module: activeModule,
                            history: chatHistory.slice(-6)
                        }),
                        signal: activeController.signal
                    });

                    typingIndicator.style.display = "none";

                    if (apiRes.ok) {
                        const data = await apiRes.json();
                        assistantResponse = data.response || "No response received.";
                        responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                        scrollToBottom();

                        const finalTime = Date.now() - startResponseTime;
                        const latencyStr = data.latency_ms && data.latency_ms.total_ms ? `${data.latency_ms.total_ms}ms` : `~${(finalTime/1000).toFixed(1)}s`;
                        metaTime.textContent = `Response: ${latencyStr} (${data.intent || 'CIH Enterprise AI'})`;
                        saveAssistantMessage(assistantResponse);
                        return;
                    }
                } catch(err) {
                    if (err.name === "AbortError") {
                        typingIndicator.style.display = "none";
                        assistantResponse = "*Generation stopped by user.*";
                        responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                        saveAssistantMessage(assistantResponse);
                        return;
                    }
                }

                // Fallback direct Ollama fetch if local API gateway unavailable
                if (ollamaStatus === "connected") {
                    try {
                        const response = await fetch("http://127.0.0.1:11434/api/chat", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                model: "llama3.2",
                                messages: callMessages,
                                stream: true,
                                options: { temperature: 0.4 }
                            }),
                            signal: activeController.signal
                        });

                        typingIndicator.style.display = "none";
                        scrollToBottom();

                        const reader = response.body.getReader();
                        const decoder = new TextDecoder("utf-8");
                        
                        while (true) {
                            const { done, value } = await reader.read();
                            if (done) break;
                            const chunk = decoder.decode(value, { stream: true });
                            const lines = chunk.split("\n");
                            for (const line of lines) {
                                if (line.trim()) {
                                    try {
                                        const parsed = JSON.parse(line);
                                        const delta = parsed.message.content;
                                        if (delta) {
                                            assistantResponse += delta;
                                            responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                                            scrollToBottom();
                                        }
                                    } catch(e) {}
                                }
                            }
                        }
                    } catch(err) {
                        typingIndicator.style.display = "none";
                        if (err.name === "AbortError") {
                            assistantResponse += "\n\n*Generation stopped by user.*";
                            responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                        } else {
                            assistantResponse += `\n\n*⚠️ Error querying Ollama: ${err.message}. Switching to simulation fallback...*`;
                            assistantResponse += getJSMockResponse(text, activeModule);
                            responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                        }
                        scrollToBottom();
                    }
                } else {
                    typingIndicator.style.display = "none";
                    scrollToBottom();
                    
                    const simulatedText = getJSMockResponse(text, activeModule);
                    let idx = 0;
                    const interval = setInterval(() => {
                        if (activeController && activeController.signal.aborted) {
                            clearInterval(interval);
                            assistantResponse += "\n\n*Generation stopped by user.*";
                            responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                            finalizeResponse();
                            return;
                        }
                        
                        const words = simulatedText.split(" ");
                        if (idx < words.length) {
                            assistantResponse += (idx === 0 ? "" : " ") + words[idx];
                            responseBubble.innerHTML = parseBasicMarkdown(assistantResponse);
                            scrollToBottom();
                            idx++;
                        } else {
                            clearInterval(interval);
                            finalizeResponse();
                        }
                    }, 40);
                    
                    const finalizeResponse = () => {
                        const finalTime = Date.now() - startResponseTime;
                        metaTime.textContent = `Response: ~${(finalTime/1000).toFixed(1)}s (Simulated)`;
                        saveAssistantMessage(assistantResponse);
                    };
                    return;
                }

                const finalTime = Date.now() - startResponseTime;
                metaTime.textContent = `Response: ~${(finalTime/1000).toFixed(1)}s (Llama 3.2)`;
                saveAssistantMessage(assistantResponse);
            };

            // Setup Context listener interval
            setInterval(() => {
                const ctxNode = hostDoc.getElementById("cih-active-context");
                const ctxDataNode = hostDoc.getElementById("cih-active-context-data");
                
                if (ctxNode && ctxDataNode) {
                    const modName = ctxNode.getAttribute("data-module");
                    const modCtx = ctxDataNode.value;
                    
                    if (modName && modName !== activeModule) {
                        activeModule = modName;
                        activeContext = modCtx;
                        moduleBadge.textContent = modName.replace(/[^a-zA-Z ]/g, "").trim();
                        renderChips(modName);
                        
                        chatHistory.push({
                            role: "assistant",
                            content: `🔄 *Context switched to **${modName}** module. Ready for queries.*`,
                            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                        });
                        localStorage.setItem("cih_floating_chat_history", JSON.stringify(chatHistory));
                        renderMessages();
                    }
                }
                syncTheme();
                updateSmartPosition();
            }, 1200);

            // Context-Aware Smart Collision Avoidance & Responsive Positioning Algorithm
            const updateSmartPosition = () => {
                if (isPinned || isDragging) return;
                const rootNodeEl = hostDoc.getElementById("cih-assistant-root");
                const fabEl = hostDoc.getElementById("cih-assistant-fab");
                const winEl = hostDoc.getElementById("cih-assistant-window");
                if (!rootNodeEl || !fabEl) return;

                const vWidth = window.innerWidth || 1920;
                const vHeight = window.innerHeight || 1080;

                let defaultBottom = 24;
                let defaultRight = 24;

                if (vWidth <= 768) {
                    defaultBottom = 12;
                    defaultRight = 12;
                } else if (vWidth <= 1366 || vHeight <= 800) {
                    defaultBottom = 18;
                    defaultRight = 18;
                }

                // Check collision with interactive page controls in parent document
                const parentDoc = window.parent ? window.parent.document : hostDoc;
                const interactiveControls = parentDoc.querySelectorAll(
                    'button, .stButton button, .stDownloadButton button, input[type="submit"], [role="button"], .cih-kpi-card, .stForm'
                );

                let collisionDetected = false;
                const fabRect = fabEl.getBoundingClientRect();

                interactiveControls.forEach(el => {
                    if (el.closest("#cih-assistant-root")) return;
                    const r = el.getBoundingClientRect();
                    if (r.width === 0 || r.height === 0) return;

                    const overlap = !(
                        r.right < fabRect.left - 12 ||
                        r.left > fabRect.right + 12 ||
                        r.bottom < fabRect.top - 12 ||
                        r.top > fabRect.bottom + 12
                    );
                    if (overlap) {
                        collisionDetected = true;
                    }
                });

                let extraBottomOffset = 0;
                const modLower = (activeModule || "").toLowerCase();
                if (modLower.includes("project") || modLower.includes("cost") || modLower.includes("material") || modLower.includes("worker") || modLower.includes("safety") || modLower.includes("report") || modLower.includes("equipment")) {
                    if (collisionDetected) {
                        extraBottomOffset = 52;
                    }
                }

                const targetBottom = defaultBottom + extraBottomOffset;
                rootNodeEl.style.bottom = `${targetBottom}px`;
                rootNodeEl.style.right = `${defaultRight}px`;
            };

            window.addEventListener("resize", updateSmartPosition);
            window.addEventListener("scroll", updateSmartPosition, true);

            // Bind UI event actions
            fab.onclick = () => {
                win.classList.toggle("minimized");
                const isExpanded = !win.classList.contains("minimized");
                fab.setAttribute("aria-expanded", isExpanded ? "true" : "false");
                if (isExpanded) {
                    scrollToBottom();
                    inputField.focus();
                }
                updateSmartPosition();
            };
            closeBtn.onclick = () => {
                win.classList.add("minimized");
                fab.setAttribute("aria-expanded", "false");
                updateSmartPosition();
            };
            clearChatBtn.onclick = () => {
                chatHistory = [{
                    role: "assistant",
                    content: `Chat history cleared. Active context: **${activeModule}**. How can I help?`,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                }];
                localStorage.setItem("cih_floating_chat_history", JSON.stringify(chatHistory));
                renderMessages();
            };
            stopBtn.onclick = () => { if (activeController) activeController.abort(); };

            inputField.addEventListener("input", function() {
                this.style.height = "auto";
                this.style.height = (this.scrollHeight - 4) + "px";
            });
            inputField.addEventListener("keydown", (e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    submitChatQuery();
                }
            });
            sendBtn.onclick = submitChatQuery;

            pinBtn.onclick = () => {
                isPinned = !isPinned;
                pinBtn.style.color = isPinned ? "#3B82F6" : "";
                updateSmartPosition();
            };

            // Dragging actions
            let isDragging = false;
            let dragX = 0, dragY = 0;
            header.onmousedown = (e) => {
                if (isPinned) return;
                if (e.target.closest(".cih-assistant-header-controls")) return;
                isDragging = true;
                const rect = win.getBoundingClientRect();
                dragX = e.clientX - rect.left;
                dragY = e.clientY - rect.top;
                
                hostDoc.onmousemove = (ev) => {
                    if (!isDragging) return;
                    const newLeft = ev.clientX - dragX;
                    const newTop = ev.clientY - dragY;
                    const right = window.innerWidth - (newLeft + rect.width);
                    const bottom = window.innerHeight - (newTop + rect.height);
                    win.style.right = `${Math.max(0, right)}px`;
                    win.style.bottom = `${Math.max(0, bottom)}px`;
                };
                
                hostDoc.onmouseup = () => {
                    isDragging = false;
                    hostDoc.onmousemove = null;
                };
            };

            // Initialize Setup
            renderChips(activeModule);
            loadHistory();
            updateSmartPosition();
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def render_page_header(title: str, subtitle: str = "") -> None:
    """Render consistent page header."""
    subtitle_html = f'<p class="cih-page-subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="cih-page-header">
            <h1 class="cih-page-title">{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, icon: str = "", delta: str = "", delta_color: str = "#22C55E") -> None:
    """Render a glassmorphism KPI card."""
    delta_html = (
        f'<div class="cih-kpi-delta" style="color:{delta_color};">{delta}</div>'
        if delta
        else ""
    )
    icon_html = f'<span class="cih-kpi-icon">{icon}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="cih-kpi-card">
            {icon_html}
            <div class="cih-kpi-label">{label}</div>
            <div class="cih-kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_badge(text: str, badge_type: str = "info") -> str:
    """Return HTML badge string."""
    return f'<span class="cih-badge cih-badge-{badge_type}">{text}</span>'


def status_to_badge(status: str) -> str:
    """Map status string to badge HTML."""
    status_lower = str(status).lower()
    mapping = {
        "active": "success",
        "completed": "info",
        "on hold": "warning",
        "delayed": "danger",
        "in progress": "info",
        "planning": "neutral",
        "high": "danger",
        "medium": "warning",
        "low": "success",
        "available": "success",
        "in use": "info",
        "maintenance": "warning",
        "critical": "danger",
        "adequate": "success",
        "low stock": "warning",
        "out of stock": "danger",
        "present": "success",
        "absent": "danger",
        "on leave": "warning",
        "compliant": "success",
        "non-compliant": "danger",
        "partial": "warning",
    }
    badge_type = mapping.get(status_lower, "neutral")
    return render_badge(status, badge_type)


def render_glass_card(title: str, content_html: str) -> None:
    """Render a titled glass card with custom HTML content."""
    st.markdown(
        f"""
        <div class="cih-glass-card">
            <div class="cih-card-title">{title}</div>
            {content_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_bar(label: str, value: float, max_value: float = 100) -> None:
    """Render animated progress bar."""
    pct = min(100, max(0, (value / max_value) * 100))
    color = "#22C55E" if pct >= 90 else "#F59E0B" if pct >= 50 else "#EF4444"
    st.markdown(
        f"""
        <div style="margin-bottom: 0.75rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.25rem;">
                <span>{label}</span><span style="color:var(--text-primary); font-weight:600;">{pct:.1f}%</span>
            </div>
            <div class="cih-progress-bar">
                <div class="cih-progress-fill" style="width:{pct}%; background: linear-gradient(90deg, {color}, {color}88);"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


import base64
from functools import lru_cache
from pathlib import Path

@lru_cache(maxsize=16)
def _get_base64_logo(logo_path: str) -> str:
    path = Path(logo_path)
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def render_sidebar_branding(logo_path: str | None = None) -> None:
    """Render sidebar brand section."""
    logo_html = ""
    if logo_path:
        encoded = _get_base64_logo(logo_path)
        if encoded:
            logo_html = (
                f'<img src="data:image/png;base64,{encoded}" '
                f'style="max-width:140px; width:auto; height:60px; max-height:60px; object-fit:contain; margin:0 auto 8px auto; display:block;" '
                f'alt="CIH Logo" />'
            )

    st.markdown(
        f"""
        <div class="cih-sidebar-brand">
            {logo_html}
            <div class="cih-sidebar-title">Agentic AI for Safety Monitoring with Construction Risk Analytics</div>
            <div class="cih-sidebar-tagline">Enterprise Construction Management Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
