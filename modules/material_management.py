"""Material management module for CIH."""

import pandas as pd
import streamlit as st

from utils import charts, dummy_data
from utils.styles import render_kpi_card, render_page_header, render_progress_bar, status_to_badge
from backend.services.material_service import material_service


def render() -> None:
    """Render material management page."""
    render_page_header("Material Management", "Track inventory, suppliers, and stock levels")

    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    active_proj_id = active_proj.id if active_proj else st.session_state.get("active_project_id")
    db_mats = material_service.get_project_materials(active_proj_id) if active_proj_id else []
    if db_mats:
        mat_rows = []
        for m in db_mats:
            stock_pct = round((m.quantity_available / max(m.quantity_required, 1.0)) * 100, 1)
            status_str = "Adequate" if stock_pct >= 75 else ("Low Stock" if stock_pct >= 30 else "Critical")
            mat_rows.append({
                "Material": m.material_name,
                "Category": m.category or "General",
                "Available": int(m.quantity_available),
                "Required": int(m.quantity_required),
                "Supplier": m.supplier or "BuildPro Supplies",
                "Cost": m.unit_cost,
                "Status": status_str,
                "Stock %": min(stock_pct, 100.0)
            })
        materials = pd.DataFrame(mat_rows)
    else:
        materials = dummy_data.get_materials(project_id=active_proj_id)

    adequate = len(materials[materials["Status"] == "Adequate"])
    low_stock = len(materials[materials["Status"] == "Low Stock"])
    critical = len(materials[materials["Status"] == "Critical"])
    total_value = (materials["Available"] * materials["Cost"]).sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Materials", str(len(materials)), "🧱")
    with col2:
        render_kpi_card("Adequate Stock", str(adequate), "✅", delta="Healthy levels", delta_color="#22C55E")
    with col3:
        render_kpi_card("Low / Critical", str(low_stock + critical), "⚠️", delta="Needs attention", delta_color="#F59E0B")
    with col4:
        render_kpi_card("Inventory Value", f"₹{total_value:,.0f}", "💰")

    tab1, tab2 = st.tabs(["📋 Inventory Table", "📊 Stock Analytics"])

    with tab1:
        st.markdown("#### Material Inventory")
        display_df = materials.copy()
        display_df["Cost"] = display_df["Cost"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(display_df.drop(columns=["Stock %"]), use_container_width=True, hide_index=True)

        st.markdown("#### Stock Progress")
        for _, row in materials.iterrows():
            st.markdown(
                f'<div style="margin-bottom:0.25rem;">'
                f'<span style="color:var(--text-primary); font-size:0.85rem;">{row["Material"]} '
                f'{status_to_badge(row["Status"])}</span></div>',
                unsafe_allow_html=True,
            )
            render_progress_bar(
                f'{row["Available"]:,} / {row["Required"]:,} units',
                row["Stock %"],
            )

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(charts.create_inventory_chart(materials), use_container_width=True)
        with col_b:
            supplier_counts = materials.groupby("Supplier").size().reset_index(name="Count")
            fig = charts.create_department_pie(supplier_counts.rename(columns={"Supplier": "Department"}))
            fig.update_layout(title=dict(text="Supplier Distribution", font=dict(color="#FFFFFF", size=14)))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="cih-glass-card">
                <div class="cih-card-title">📦 Reorder Recommendations</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        reorder = materials[materials["Status"].isin(["Low Stock", "Critical"])]
        if len(reorder) > 0:
            for _, row in reorder.iterrows():
                deficit = row["Required"] - row["Available"]
                st.warning(f"⚠️ **{row['Material']}**: Order {deficit:,} units from {row['Supplier']}")
        else:
            st.success("✅ All materials are at adequate stock levels")
