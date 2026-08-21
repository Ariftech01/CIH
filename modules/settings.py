"""Settings module for CIH."""

import streamlit as st

from utils.styles import render_glass_card, render_page_header


def render() -> None:
    """Render settings page."""
    render_page_header("Settings", "Configure application preferences and system options")

    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Theme", "🔔 Notifications", "🌐 Language", "👤 User Preferences"])

    with tab1:
        st.markdown("#### Appearance Settings")
        current_theme = st.session_state.get("theme", "Dark")
        theme_index = 0 if current_theme == "Dark" else 1
        selected_theme_label = st.selectbox("Theme", ["Dark (Default)", "Light"], index=theme_index)
        selected_theme = "Dark" if selected_theme_label == "Dark (Default)" else "Light"

        if selected_theme != current_theme:
            st.session_state.theme = selected_theme
            st.rerun()

        accent_color = st.color_picker("Accent Color", "#3B82F6")
        compact_mode = st.toggle("Compact Mode", value=False)
        animations = st.toggle("Enable Animations", value=True)

        preview_bg = "linear-gradient(135deg, #0F172A, #1E293B)" if selected_theme == "Dark" else "linear-gradient(135deg, #F8FAFC, #E2E8F0)"
        preview_text_color = "#FFFFFF" if selected_theme == "Dark" else "#0F172A"
        preview_label_color = "#94A3B8" if selected_theme == "Dark" else "#475569"

        st.markdown(
            f"""
            <div class="cih-glass-card">
                <div class="cih-card-title">Theme Preview</div>
                <div style="padding:1rem; border-radius:12px; background:{preview_bg}; border: 1px solid var(--card-border);">
                    <div style="color:{preview_text_color}; font-weight:600;">{selected_theme} Theme Active</div>
                    <div style="color:{preview_label_color}; font-size:0.85rem; margin-top:0.25rem;">Accent: {accent_color}</div>
                    <div style="margin-top:0.75rem; padding:0.5rem 1rem; background:{accent_color}; border-radius:8px; display:inline-block; color:#FFF; font-size:0.85rem; font-weight:600;">Sample Button</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("💾 Save Theme Settings", use_container_width=True):
            st.success("✅ Theme settings saved successfully")

    with tab2:
        st.markdown("#### Notification Preferences")
        st.toggle("Email Notifications", value=True)
        st.toggle("Push Notifications", value=True)
        st.toggle("Safety Alerts", value=True)
        st.toggle("Budget Threshold Alerts", value=True)
        st.toggle("Deadline Reminders", value=True)
        st.toggle("Inventory Low Stock Alerts", value=True)

        st.selectbox("Notification Frequency", ["Real-time", "Hourly Digest", "Daily Digest", "Weekly Summary"])

        if st.button("💾 Save Notification Settings", use_container_width=True):
            st.success("✅ Notification preferences updated")

    with tab3:
        st.markdown("#### Language & Region")
        language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali"])
        timezone = st.selectbox("Timezone", ["Asia/Kolkata (IST)", "UTC", "Asia/Dubai", "Europe/London"])
        date_format = st.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])

        render_glass_card(
            "Current Configuration",
            f'<div class="cih-metric-row"><span class="cih-metric-label">Language</span><span class="cih-metric-value">{language}</span></div>'
            f'<div class="cih-metric-row"><span class="cih-metric-label">Timezone</span><span class="cih-metric-value">{timezone}</span></div>'
            f'<div class="cih-metric-row"><span class="cih-metric-label">Date Format</span><span class="cih-metric-value">{date_format}</span></div>'
            f'<div class="cih-metric-row"><span class="cih-metric-label">Currency</span><span class="cih-metric-value">{currency}</span></div>',
        )

        if st.button("💾 Save Language Settings", use_container_width=True):
            st.success("✅ Language settings saved")

    with tab4:
        st.markdown("#### User Profile")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", value="Admin User")
            st.text_input("Email", value="admin@cih.enterprise")
            st.text_input("Department", value="Project Management")
        with col2:
            st.text_input("Employee ID", value="EMP-001")
            st.selectbox("Role", ["Administrator", "Project Manager", "Site Engineer", "Viewer"])
            st.selectbox("Default Dashboard", ["Executive", "Project", "Safety", "Operations"])

        if st.button("💾 Save User Preferences", use_container_width=True):
            st.success("✅ User preferences saved")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="cih-glass-card">
            <div class="cih-card-title">ℹ Application Information</div>
            <div class="cih-metric-row"><span class="cih-metric-label">Application</span><span class="cih-metric-value">Agentic AI for Safety Monitoring with Construction Risk Analytics</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Version</span><span class="cih-metric-value">1.0.0</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Framework</span><span class="cih-metric-value">Streamlit</span></div>
            <div class="cih-metric-row"><span class="cih-metric-label">Environment</span><span class="cih-metric-value">Frontend Prototype</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
