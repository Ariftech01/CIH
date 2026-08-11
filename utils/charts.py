"""Plotly chart builders for CIH dashboard."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94A3B8", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0")),
)

COLORS = ["#3B82F6", "#60A5FA", "#22C55E", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]


def _apply_layout(fig: go.Figure, title: str = "", height: int = 350) -> go.Figure:
    """Apply consistent theme-aware layout."""
    import streamlit as st
    theme = st.session_state.get("theme", "Dark")
    
    if theme == "Light":
        font_color = "#475569"
        title_color = "#0F172A"
        legend_color = "#1E293B"
        grid_color = "rgba(15, 23, 42, 0.08)"
    else:
        font_color = "#94A3B8"
        title_color = "#FFFFFF"
        legend_color = "#E2E8F0"
        grid_color = "rgba(255, 255, 255, 0.06)"
        
    layout = {
        **CHART_LAYOUT,
        "height": height,
        "font": dict(family="Inter, sans-serif", color=font_color, size=12),
        "legend": dict(bgcolor="rgba(0,0,0,0)", font=dict(color=legend_color)),
    }
    if title:
        layout["title"] = dict(text=title, font=dict(color=title_color, size=14))
        
    fig.update_layout(**layout)
    fig.update_xaxes(gridcolor=grid_color, zerolinecolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color, zerolinecolor=grid_color)
    return fig


def create_timeline_chart(df: pd.DataFrame) -> go.Figure:
    """Line chart for project timeline."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["Planned"], name="Planned",
        line=dict(color="#3B82F6", width=3), mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["Actual"], name="Actual",
        line=dict(color="#22C55E", width=3), mode="lines+markers",
        fill="tonexty", fillcolor="rgba(34, 197, 94, 0.1)",
    ))
    return _apply_layout(fig, "Project Timeline", 380)


def create_budget_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Pie chart for budget allocation."""
    fig = px.pie(
        df, values="Amount", names="Category",
        color_discrete_sequence=COLORS,
        hole=0.35,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
    return _apply_layout(fig, "Budget Allocation", 380)


def create_status_donut_chart(df: pd.DataFrame) -> go.Figure:
    """Donut chart for project status."""
    fig = px.pie(
        df, values="Count", names="Status",
        color_discrete_sequence=COLORS,
        hole=0.55,
    )
    fig.update_traces(textposition="inside", textinfo="value+label")
    return _apply_layout(fig, "Project Status", 380)


def create_worker_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart for worker distribution."""
    fig = px.bar(
        df, x="Department", y="Count",
        color="Count", color_continuous_scale=["#1E40AF", "#3B82F6", "#60A5FA"],
    )
    fig.update_coloraxes(showscale=False)
    return _apply_layout(fig, "Worker Distribution", 380)


def create_equipment_usage_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart for equipment usage."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Equipment"], y=df["Hours"],
        name="Operating Hours",
        marker_color="#3B82F6",
        marker_line=dict(width=0),
    ))
    fig.add_trace(go.Scatter(
        x=df["Equipment"], y=df["Utilization"],
        name="Utilization %", yaxis="y2",
        line=dict(color="#F59E0B", width=3), mode="lines+markers",
    ))
    fig.update_layout(
        yaxis2=dict(title="Utilization %", overlaying="y", side="right", gridcolor="rgba(0,0,0,0)"),
    )
    return _apply_layout(fig, "Equipment Usage", 380)


def create_inventory_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart for material inventory levels."""
    fig = px.bar(
        df, x="Material", y="Stock %",
        color="Stock %",
        color_continuous_scale=["#EF4444", "#F59E0B", "#22C55E"],
    )
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(tickangle=-45)
    return _apply_layout(fig, "Material Stock Levels", 400)


def create_safety_gauge(score: float) -> go.Figure:
    """Gauge chart for safety score."""
    import streamlit as st
    theme = st.session_state.get("theme", "Dark")
    is_light = theme == "Light"
    
    text_color = "#0F172A" if is_light else "#FFFFFF"
    gauge_bg = "rgba(15, 23, 42, 0.05)" if is_light else "rgba(255,255,255,0.05)"
    line_color = "#0F172A" if is_light else "#FFFFFF"
    
    color = "#22C55E" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={"reference": 90, "increasing": {"color": "#22C55E"}},
        number={"font": {"color": text_color, "size": 42}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#64748B"},
            "bar": {"color": color},
            "bgcolor": gauge_bg,
            "borderwidth": 0,
            "steps": [
                {"range": [0, 60], "color": "rgba(239, 68, 68, 0.2)"},
                {"range": [60, 80], "color": "rgba(245, 158, 11, 0.2)"},
                {"range": [80, 100], "color": "rgba(34, 197, 94, 0.2)"},
            ],
            "threshold": {"line": {"color": line_color, "width": 2}, "thickness": 0.75, "value": 90},
        },
        title={"text": "Safety Score", "font": {"color": "#64748B" if is_light else "#94A3B8", "size": 14}},
    ))
    return _apply_layout(fig, "", 320)


def create_risk_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart for risk distribution."""
    color_map = {"Low": "#22C55E", "Medium": "#F59E0B", "High": "#EF4444", "Critical": "#DC2626"}
    colors = [color_map.get(r, "#3B82F6") for r in df["Risk Level"]]
    fig = go.Figure(go.Bar(
        x=df["Risk Level"], y=df["Count"],
        marker_color=colors, marker_line=dict(width=0),
    ))
    return _apply_layout(fig, "Risk Distribution", 350)


def create_attendance_chart(df: pd.DataFrame) -> go.Figure:
    """Stacked bar chart for attendance."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["Day"], y=df["Present"], name="Present", marker_color="#22C55E"))
    fig.add_trace(go.Bar(x=df["Day"], y=df["Absent"], name="Absent", marker_color="#EF4444"))
    fig.update_layout(barmode="stack")
    return _apply_layout(fig, "Weekly Attendance", 350)


def create_department_pie(df: pd.DataFrame) -> go.Figure:
    """Pie chart for department distribution."""
    value_col = "Count"
    if "Count" not in df.columns:
        other_cols = [c for c in df.columns if c != "Department"]
        if other_cols:
            value_col = other_cols[0]
    fig = px.pie(df, values=value_col, names="Department", color_discrete_sequence=COLORS)
    return _apply_layout(fig, "Department Distribution", 350)


def create_weekly_progress_chart(df: pd.DataFrame) -> go.Figure:
    """Area chart for weekly progress."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Week"], y=df["Progress"],
        fill="tozeroy", fillcolor="rgba(59, 130, 246, 0.2)",
        line=dict(color="#3B82F6", width=3), mode="lines+markers", name="Progress",
    ))
    return _apply_layout(fig, "Weekly Progress", 350)


def create_monthly_progress_chart(df: pd.DataFrame) -> go.Figure:
    """Line chart comparing target vs actual."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["Target"], name="Target",
        line=dict(color="#94A3B8", width=2, dash="dash"), mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["Actual"], name="Actual",
        line=dict(color="#3B82F6", width=3), mode="lines+markers",
    ))
    return _apply_layout(fig, "Monthly Progress", 350)


def create_gantt_placeholder(milestones: pd.DataFrame) -> go.Figure:
    """Gantt-style timeline chart for milestones."""
    fig = go.Figure()
    colors = {"Completed": "#22C55E", "In Progress": "#3B82F6", "Planning": "#64748B"}
    for _, row in milestones.iterrows():
        fig.add_trace(go.Bar(
            x=[(pd.to_datetime(row["End"]) - pd.to_datetime(row["Start"])).days],
            y=[row["Milestone"]],
            orientation="h",
            name=row["Status"],
            marker_color=colors.get(row["Status"], "#3B82F6"),
            text=f"{row['Progress']}%",
            textposition="inside",
            showlegend=False,
        ))
    return _apply_layout(fig, "Project Milestones (Gantt View)", 400)


def create_cost_breakdown_chart(
    material: float, labour: float, tax: float, contingency: float,
) -> go.Figure:
    """Pie chart for cost estimation breakdown."""
    df = pd.DataFrame({
        "Category": ["Material", "Labour", "Tax", "Contingency"],
        "Amount": [material, labour, tax, contingency],
    })
    fig = px.pie(df, values="Amount", names="Category", color_discrete_sequence=COLORS, hole=0.4)
    return _apply_layout(fig, "Cost Breakdown", 350)
