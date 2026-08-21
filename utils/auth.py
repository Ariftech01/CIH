"""Authentication service and UI components for Agentic AI for Safety Monitoring with Construction Risk Analytics."""

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
        /* Disable page and container scrollbars on login screen */
        html, body, .stApp, 
        [data-testid="stAppViewContainer"], 
        [data-testid="stAppViewBlockContainer"], 
        [data-testid="stMainBlockContainer"],
        section.main, 
        .main, 
        .main .block-container,
        .stMain {
            overflow: hidden !important;
            overflow-y: hidden !important;
            overflow-x: hidden !important;
            height: 100vh !important;
            max-height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Hide header, sidebar, footer, and sidebar collapse controls on login page */
        header[data-testid="stHeader"],
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        section[data-testid="stSidebar"],
        footer {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
            visibility: hidden !important;
        }

        /* Center container perfectly without overflow */
        .main .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            height: 100vh !important;
            max-height: 100vh !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
        }

        /* Make custom component iframe 0 size and fixed off-screen so it does not affect layout */
        iframe[data-testid="stCustomComponentV1"],
        [data-testid="stCustomComponentV1"] {
            position: fixed !important;
            top: -9999px !important;
            left: -9999px !important;
            width: 0 !important;
            height: 0 !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* Streamlit form column width / centering */
        div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
            margin: 0 auto !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* Enterprise Login Card Styling */
        .login-card-header {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .login-title {
            color: #FFFFFF;
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.35;
            letter-spacing: -0.02em;
            margin-top: 0.5rem;
            margin-bottom: 0.35rem;
        }

        .login-subtitle {
            color: #94A3B8;
            font-size: 0.875rem;
            font-weight: 400;
            margin-bottom: 0.75rem;
        }

        /* Streamlit form customization for login */
        div[data-testid="stForm"] {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 1.75rem 2.25rem 1.5rem 2.25rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(16px);
            width: 100%;
            max-width: 480px;
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

        /* Ensure floating assistant is hidden on login page */
        #cih-assistant-root,
        #cih-assistant-bubble,
        #cih-assistant-panel,
        .cih-assistant-widget {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_page() -> None:
    """Render the enterprise login page as a non-scrolling constant screen with keyboard Enter navigation."""
    inject_login_styles()

    # Ensure floating AI assistant is removed/suppressed on the login page and handle keyboard navigation
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
        (function() {
            const hostDoc = window.parent.document || document;

            // 1. Ensure floating assistant artifacts are purged from Login page
            const rootNode = hostDoc.getElementById("cih-assistant-root");
            if (rootNode) {
                rootNode.style.display = "none";
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

            // 2. Setup Keyboard Navigation and Enter Flow
            function setupLoginKeyboardFlow() {
                const usernameInput = hostDoc.querySelector('input[aria-label="Username"]') || 
                                      hostDoc.querySelector('input[placeholder="Enter your username"]');
                const passwordInput = hostDoc.querySelector('input[aria-label="Password"]') || 
                                      hostDoc.querySelector('input[placeholder="Enter your password"]');
                const submitBtn = hostDoc.querySelector('div[data-testid="stFormSubmitButton"] button') || 
                                  hostDoc.querySelector('button[type="submit"]');

                if (!usernameInput || !passwordInput) {
                    return false;
                }

                // Get or create validation message banner inside the form
                const formEl = usernameInput.closest('form') || hostDoc.querySelector('div[data-testid="stForm"]');
                let valBanner = hostDoc.getElementById("cih-login-val-banner");
                if (!valBanner && formEl) {
                    valBanner = hostDoc.createElement("div");
                    valBanner.id = "cih-login-val-banner";
                    valBanner.style.display = "none";
                    valBanner.style.color = "#FCA5A5";
                    valBanner.style.backgroundColor = "rgba(239, 68, 68, 0.15)";
                    valBanner.style.border = "1px solid rgba(239, 68, 68, 0.4)";
                    valBanner.style.borderRadius = "8px";
                    valBanner.style.padding = "0.5rem 0.75rem";
                    valBanner.style.fontSize = "0.85rem";
                    valBanner.style.marginTop = "0.5rem";
                    valBanner.style.marginBottom = "0.5rem";
                    valBanner.style.textAlign = "center";
                    valBanner.style.fontWeight = "500";

                    const submitContainer = hostDoc.querySelector('div[data-testid="stFormSubmitButton"]');
                    if (submitContainer && submitContainer.parentNode) {
                        submitContainer.parentNode.insertBefore(valBanner, submitContainer);
                    } else {
                        formEl.appendChild(valBanner);
                    }
                }

                function showValidation(msg, targetInput) {
                    if (valBanner) {
                        valBanner.textContent = msg;
                        valBanner.style.display = "block";
                    }
                    if (targetInput) {
                        targetInput.focus();
                    }
                }

                function hideValidation() {
                    if (valBanner) {
                        valBanner.style.display = "none";
                    }
                }

                // Clear client-side validation on typing
                if (!usernameInput._cihInputBound) {
                    usernameInput.addEventListener("input", hideValidation);
                    usernameInput._cihInputBound = true;
                }
                if (!passwordInput._cihInputBound) {
                    passwordInput.addEventListener("input", hideValidation);
                    passwordInput._cihInputBound = true;
                }

                // Intercept Enter key
                function handleKeyDown(e) {
                    if (e.key !== "Enter" && e.keyCode !== 13) {
                        return;
                    }

                    const curActive = hostDoc.activeElement;
                    const isUser = (curActive === usernameInput || usernameInput === e.target);
                    const isPass = (curActive === passwordInput || passwordInput === e.target);

                    if (!isUser && !isPass) {
                        return;
                    }

                    const uVal = (usernameInput.value || "").trim();
                    const pVal = (passwordInput.value || "");

                    if (isUser) {
                        // ALWAYS prevent form submission on Username Enter
                        e.preventDefault();
                        e.stopPropagation();
                        e.stopImmediatePropagation();

                        if (!uVal) {
                            // Empty username: show validation, keep focus
                            showValidation("Please enter username", usernameInput);
                            usernameInput.focus();
                        } else {
                            // Username entered: move focus to Password field
                            hideValidation();
                            passwordInput.focus();
                            passwordInput.select();
                        }
                        return false;
                    }

                    if (isPass) {
                        if (!uVal) {
                            // Empty username when pressing Enter in Password field
                            e.preventDefault();
                            e.stopPropagation();
                            e.stopImmediatePropagation();
                            showValidation("Please enter username", usernameInput);
                            usernameInput.focus();
                            return false;
                        }

                        if (!pVal) {
                            // Empty password when pressing Enter in Password field
                            e.preventDefault();
                            e.stopPropagation();
                            e.stopImmediatePropagation();
                            showValidation("Please enter password", passwordInput);
                            passwordInput.focus();
                            return false;
                        }

                        // Both fields non-empty: Submit login form (Sign In action)
                        hideValidation();
                        e.preventDefault();
                        e.stopPropagation();
                        if (submitBtn) {
                            submitBtn.click();
                        }
                        return false;
                    }
                }

                if (hostDoc._cihLoginKeydownHandler) {
                    hostDoc.removeEventListener("keydown", hostDoc._cihLoginKeydownHandler, true);
                }
                hostDoc._cihLoginKeydownHandler = handleKeyDown;
                hostDoc.addEventListener("keydown", handleKeyDown, true);

                return true;
            }

            setupLoginKeyboardFlow();
            let attempts = 0;
            const interval = setInterval(function() {
                attempts++;
                if (setupLoginKeyboardFlow() || attempts > 20) {
                    clearInterval(interval);
                }
            }, 150);
        })();
        </script>
        """,
        height=0,
        width=0,
    )

    # Center column layout
    left_col, main_col, right_col = st.columns([1, 2.2, 1])

    with main_col:
        with st.form(key="cih_login_form", clear_on_submit=False):
            # Logo header
            if LOGO_PATH.exists():
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 0.25rem;">
                        <img src="data:image/png;base64,{_get_logo_base64()}" style="max-width: 165px; width: 100%; height: auto; display: inline-block;" alt="CIH Logo" />
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
                    <div class="login-title">Agentic AI for Safety Monitoring with Construction Risk Analytics</div>
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
                clean_username = username.strip() if username else ""
                if not clean_username:
                    st.error("Please enter username")
                elif not password:
                    st.error("Please enter password")
                elif authenticate_user(clean_username, password):
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "username": clean_username,
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
    if st.button("🚪 Logout", key="logout_button", use_container_width=True):
        logout()
