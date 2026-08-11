"""Authentication service and UI components for Construction Intelligence Hub (CIH)."""

from pathlib import Path
import streamlit as st

# Root directory path for assets
ROOT = Path(__file__).parent.parent
LOGO_PATH = ROOT / "assets" / "logo.png"

# Default enterprise credentials (Case-sensitive)
DEFAULT_USERNAME = "Admin"
DEFAULT_PASSWORD = "Admin@123"


def init_auth_session() -> None:
    """Initialize authentication session state keys."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None


def is_authenticated() -> bool:
    """Check if current session is authenticated."""
    return st.session_state.get("authenticated", False)


def logout() -> None:
    """Clear authentication session and transient project context state, then rerun application."""
    keys_to_clear = [
        "authenticated",
        "user",
        "active_project_id",
        "active_project_code",
        "active_project_name",
        "_active_project_obj",
        "sidebar_active_project_selector",
        "detail_project",
        "project_form_draft",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def authenticate_user(username: str, password: str) -> bool:
    """
    Validate user credentials.
    Designed to be future-ready for multi-user or database authentication.
    """
    # Strict case-sensitive comparison
    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        return True
    return False


def inject_login_styles() -> None:
    """Inject custom styles for hiding the sidebar and rendering a constant fixed login page without scrollbars."""
    st.markdown(
        """
        <style>
        /* Disable page scrollbar on login screen */
        html, body, .stApp, [data-testid="stAppViewContainer"], section.main {
            overflow: hidden !important;
            height: 100vh !important;
            max-height: 100vh !important;
        }

        /* Hide header, sidebar, and sidebar collapse controls on login page */
        header[data-testid="stHeader"],
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }

        /* Center container perfectly without overflow */
        .main .block-container {
            max-width: 100% !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            height: 100vh !important;
            max-height: 100vh !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            overflow: hidden !important;
        }

        /* Enterprise Login Card Styling */
        .login-card-header {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .login-title {
            color: #FFFFFF;
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-top: 0.5rem;
            margin-bottom: 0.25rem;
        }

        .login-subtitle {
            color: #94A3B8;
            font-size: 0.85rem;
            font-weight: 400;
            margin-bottom: 1rem;
        }

        /* Streamlit form customization for login */
        div[data-testid="stForm"] {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 1.75rem 2rem 1.5rem 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(16px);
            width: 100%;
            max-width: 440px;
            margin: 0 auto;
        }

        div[data-testid="stForm"] button[type="submit"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.55rem 1rem !important;
            margin-top: 0.75rem !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
        }

        div[data-testid="stForm"] button[type="submit"]:hover {
            background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5) !important;
            transform: translateY(-1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_page() -> None:
    """Render the enterprise login page as a non-scrolling constant screen."""
    inject_login_styles()

    # Center column layout
    left_col, main_col, right_col = st.columns([1, 1.4, 1])

    with main_col:
        with st.form(key="cih_login_form", clear_on_submit=False):
            # Logo header
            if LOGO_PATH.exists():
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,{_get_logo_base64()}" style="max-width: 90px; height: auto;" alt="CIH Logo" />
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div style="text-align: center; font-size: 2.5rem;">🏗️</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                """
                <div class="login-card-header">
                    <div class="login-title">Construction Intelligence Hub</div>
                    <div class="login-subtitle">Enterprise Construction Management Platform</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Username",
                key="input_username",
                placeholder="Enter your username",
            )

            password = st.text_input(
                "Password",
                type="password",
                key="input_password",
                placeholder="Enter your password",
            )

            submit_button = st.form_submit_button(
                label="Sign In", use_container_width=True
            )

            if submit_button:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "username": username,
                        "role": "Admin",
                    }
                    st.rerun()
                else:
                    st.error("Invalid username or password.")


def _get_logo_base64() -> str:
    """Helper function to encode logo to base64 for reliable HTML embedding."""
    import base64

    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    return ""


def render_logout_button() -> None:
    """Render a styled Logout button in the sidebar footer."""
    st.markdown(
        """
        <style>
        div.stButton > button[key="logout_button"] {
            background-color: rgba(239, 68, 68, 0.1) !important;
            color: #EF4444 !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button[key="logout_button"]:hover {
            background-color: rgba(239, 68, 68, 0.2) !important;
            border-color: rgba(239, 68, 68, 0.6) !important;
            color: #F87171 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🚪 Logout", key="logout_button", use_container_width=True):
        logout()
