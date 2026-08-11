"""Realistic dummy data generators for CIH prototype with high-performance Streamlit caching."""

from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st


def _random_dates(start_year: int = 2024, count: int = 1) -> list[datetime]:
    """Generate random dates within a range."""
    base = datetime(start_year, 1, 1)
    return [base + timedelta(days=int(np.random.randint(0, 730))) for _ in range(count)]


@st.cache_data(ttl=600, show_spinner=False)
def get_projects(count: int = 25) -> pd.DataFrame:
    """Generate sample construction projects."""
    np.random.seed(42)
    clients = [
        "L&T Construction", "Shapoorji Pallonji", "Tata Projects", "GMR Group",
        "Afcons Infrastructure", "NCC Limited", "HCC Ltd", "DLF Limited",
        "Prestige Group", "Godrej Properties", "Lodha Group", "Brigade Group",
    ]
    locations = [
        "Mumbai, MH", "Bangalore, KA", "Hyderabad, TS", "Chennai, TN",
        "Pune, MH", "Delhi NCR", "Ahmedabad, GJ", "Kolkata, WB",
        "Jaipur, RJ", "Kochi, KL", "Chandigarh, CH", "Visakhapatnam, AP",
    ]
    statuses = ["Active", "Completed", "On Hold", "Delayed", "Planning"]
    priorities = ["High", "Medium", "Low"]
    project_types = [
        "Metro Rail Phase", "Commercial Tower", "Residential Complex",
        "Highway Expansion", "Industrial Park", "Smart City Block",
        "Hospital Wing", "Airport Terminal", "Bridge Construction", "Data Center",
    ]

    rows = []
    for i in range(1, count + 1):
        start = datetime(2024, 1, 1) + timedelta(days=int(np.random.randint(0, 400)))
        duration = int(np.random.randint(180, 720))
        end = start + timedelta(days=duration)
        progress = int(np.random.randint(5, 100))
        status = np.random.choice(statuses, p=[0.35, 0.25, 0.1, 0.15, 0.15])
        if status == "Completed":
            progress = 100
        budget = round(np.random.uniform(5_000_000, 150_000_000), 2)
        rows.append({
            "Project ID": f"PRJ-{i:04d}",
            "Project Name": f"{np.random.choice(project_types)} - {np.random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega'])}",
            "Client": np.random.choice(clients),
            "Location": np.random.choice(locations),
            "Start Date": start.strftime("%Y-%m-%d"),
            "End Date": end.strftime("%Y-%m-%d"),
            "Budget": budget,
            "Progress": progress,
            "Status": status,
            "Priority": np.random.choice(priorities, p=[0.3, 0.5, 0.2]),
            "Manager": np.random.choice([
                "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy",
                "Vikram Singh", "Ananya Iyer", "Mohammed Ali", "Deepak Gupta",
            ]),
            "Description": "Large-scale construction initiative with phased delivery milestones.",
        })
    return pd.DataFrame(rows)


def _get_project_seed(project_id: str | None, base_seed: int) -> int:
    """Generate a stable integer random seed from project_id and base seed."""
    if not project_id:
        return base_seed
    return (abs(hash(str(project_id))) % 99991) + base_seed


@st.cache_data(ttl=600, show_spinner=False)
def get_workers(count: int = 40, project_id: str | None = None) -> pd.DataFrame:
    """Generate sample worker records."""
    np.random.seed(_get_project_seed(project_id, 43))
    roles = [
        "Site Engineer", "Foreman", "Electrician", "Plumber", "Mason",
        "Crane Operator", "Safety Officer", "Surveyor", "Welder", "Laborer",
        "Project Manager", "Quality Inspector",
    ]
    departments = ["Engineering", "Operations", "Safety", "Electrical", "Civil", "Mechanical"]
    statuses = ["Present", "Absent", "On Leave"]
    names = [
        "Arjun Mehta", "Kavita Nair", "Rahul Desai", "Meera Joshi", "Sanjay Verma",
        "Lakshmi Rao", "Imran Khan", "Pooja Shah", "Harish Menon", "Divya Pillai",
        "Naveen Reddy", "Swati Kulkarni", "Gopal Das", "Rekha Bansal", "Farhan Sheikh",
        "Anil Choudhury", "Bhavna Trivedi", "Chetan Malhotra", "Disha Agarwal", "Eshan Bose",
        "Falguni Deshpande", "Gaurav Saxena", "Hema Krishnan", "Irfan Qureshi", "Jyoti Pandey",
        "Karan Bhatia", "Leela Narayan", "Manish Thakur", "Neha Kapoor", "Omkar Patil",
        "Pradeep Yadav", "Quinn Fernandes", "Ravi Shankar", "Sunita Devi", "Tarun Mishra",
        "Uma Rangan", "Varun Hegde", "Waseem Ahmed", "Xavier D'Souza", "Yash Malviya",
    ]

    rows = []
    for i in range(1, count + 1):
        attendance = int(np.random.randint(70, 100))
        performance = round(np.random.uniform(3.0, 5.0), 1)
        rows.append({
            "Worker ID": f"WRK-{i:04d}",
            "Name": names[(i - 1) % len(names)],
            "Role": np.random.choice(roles),
            "Department": np.random.choice(departments),
            "Attendance": f"{attendance}%",
            "Experience": f"{np.random.randint(1, 25)} yrs",
            "Status": np.random.choice(statuses, p=[0.75, 0.1, 0.15]),
            "Performance": performance,
        })
    return pd.DataFrame(rows)


@st.cache_data(ttl=600, show_spinner=False)
def get_materials(project_id: str | None = None) -> pd.DataFrame:
    """Generate material inventory data."""
    np.random.seed(_get_project_seed(project_id, 44))
    materials = [
        ("Steel Rebar (TMT)", "Tata Steel", 1100, 1200, 68000),
        ("Portland Cement", "UltraTech", 4800, 5000, 380),
        ("Red Bricks", "Local Supplier", 35000, 100000, 8.5),
        ("River Sand", "Sand Corp", 380, 400, 4500),
        ("Crushed Aggregate", "Quarry Ltd", 580, 700, 2200),
        ("Ready Mix Concrete", "ACC RMC", 100, 250, 5200),
        ("Structural Timber", "Wood Works", 45, 60, 35000),
        ("PVC Pipes", "Finolex", 1400, 1500, 420),
        ("Electrical Cables", "Polycab", 8500, 10000, 95),
        ("Safety Netting", "SafeGuard", 150, 400, 180),
        ("Scaffolding Pipes", "ScaffPro", 750, 800, 650),
        ("Waterproofing Membrane", "Dr. Fixit", 95, 120, 28000),
    ]
    rows = []
    for name, supplier, base_avail, base_req, cost in materials:
        var_factor = np.random.uniform(0.7, 1.3)
        available = int(base_avail * var_factor)
        required = int(base_req * var_factor)
        ratio = available / max(required, 1)
        if ratio >= 0.9:
            status = "Adequate"
        elif ratio >= 0.5:
            status = "Low Stock"
        else:
            status = "Critical"
        rows.append({
            "Material": name,
            "Available": available,
            "Required": required,
            "Supplier": supplier,
            "Cost": cost,
            "Status": status,
            "Stock %": round(ratio * 100, 1),
        })
    return pd.DataFrame(rows)


@st.cache_data(ttl=600, show_spinner=False)
def get_equipment(project_id: str | None = None) -> list[dict[str, Any]]:
    """Generate equipment tracking data."""
    np.random.seed(_get_project_seed(project_id, 45))
    equipment_list = [
        {"name": "Excavator", "id": "EQ-001", "icon": "🚜"},
        {"name": "Crane", "id": "EQ-002", "icon": "🏗️"},
        {"name": "Bulldozer", "id": "EQ-003", "icon": "🚧"},
        {"name": "Concrete Mixer", "id": "EQ-004", "icon": "🔄"},
        {"name": "Dump Truck", "id": "EQ-005", "icon": "🚛"},
    ]
    availability_opts = ["Available", "In Use", "Maintenance"]
    result = []
    for eq in equipment_list:
        health = int(np.random.randint(65, 100))
        fuel = int(np.random.randint(20, 100))
        hours = int(np.random.randint(500, 5000))
        result.append({
            **eq,
            "Health": health,
            "Maintenance": "Scheduled" if health < 80 else "Up to Date",
            "Availability": np.random.choice(availability_opts, p=[0.4, 0.45, 0.15]),
            "Fuel Level": fuel,
            "Operating Hours": hours,
            "Last Service": (datetime.now() - timedelta(days=int(np.random.randint(5, 60)))).strftime("%Y-%m-%d"),
        })
    return result


@st.cache_data(ttl=600, show_spinner=False)
def get_recent_activities() -> list[dict[str, str]]:
    """Generate recent activity feed."""
    return [
        {"time": "10 min ago", "text": "Steel delivery confirmed for PRJ-0012 — Metro Rail Phase Alpha"},
        {"time": "32 min ago", "text": "Safety inspection completed at Hyderabad site — Score: 94%"},
        {"time": "1 hr ago", "text": "Budget revision approved for Commercial Tower Beta (+2.3%)"},
        {"time": "2 hrs ago", "text": "Crane EQ-002 scheduled for maintenance on Jul 8, 2026"},
        {"time": "3 hrs ago", "text": "Milestone 'Foundation Complete' achieved — PRJ-0007"},
        {"time": "5 hrs ago", "text": "15 new workers onboarded to Civil department"},
        {"time": "Yesterday", "text": "Monthly progress report generated for all active projects"},
        {"time": "Yesterday", "text": "Cement inventory alert resolved — stock replenished"},
    ]


@st.cache_data(ttl=600, show_spinner=False)
def get_upcoming_deadlines() -> pd.DataFrame:
    """Generate upcoming project deadlines."""
    np.random.seed(46)
    projects = get_projects(10)
    active = projects[projects["Status"].isin(["Active", "Delayed"])].head(6)
    rows = []
    for _, row in active.iterrows():
        deadline = datetime.strptime(row["End Date"], "%Y-%m-%d")
        days_left = (deadline - datetime.now()).days
        rows.append({
            "Project": row["Project Name"][:35],
            "Deadline": row["End Date"],
            "Days Left": max(days_left, 0),
            "Progress": f"{row['Progress']}%",
            "Priority": row["Priority"],
        })
    return pd.DataFrame(rows)


@st.cache_data(ttl=600, show_spinner=False)
def get_notifications() -> list[dict[str, str]]:
    """Generate system notifications."""
    return [
        {"type": "warning", "message": "Low stock alert: River Sand below threshold"},
        {"type": "info", "message": "Weekly safety audit scheduled for Monday"},
        {"type": "success", "message": "PRJ-0003 milestone completed ahead of schedule"},
        {"type": "danger", "message": "PRJ-0018 flagged as delayed — review required"},
        {"type": "info", "message": "New compliance guidelines available in Safety module"},
    ]


@st.cache_data(ttl=600, show_spinner=False)
def get_safety_incidents(project_id: str | None = None) -> pd.DataFrame:
    """Generate safety incident records."""
    np.random.seed(_get_project_seed(project_id, 48))
    inc_types = ["Minor Injury", "Equipment Malfunction", "Near Miss", "PPE Violation", "Scaffolding Issue"]
    severities = ["Low", "Medium", "High"]
    statuses = ["Resolved", "Under Review", "Closed", "Action Taken", "Open"]
    rows = []
    for i in range(1, 6):
        rows.append({
            "ID": f"INC-{i:03d}",
            "Date": (datetime.now() - timedelta(days=int(np.random.randint(1, 45)))).strftime("%Y-%m-%d"),
            "Type": np.random.choice(inc_types),
            "Location": f"Site {chr(64 + i)}",
            "Severity": np.random.choice(severities),
            "Status": np.random.choice(statuses),
        })
    return pd.DataFrame(rows)


def get_safety_checklist() -> dict[str, bool]:
    """Default safety checklist state."""
    return {
        "Helmet": True,
        "Boots": True,
        "Gloves": True,
        "Harness": False,
        "Fire Equipment": True,
        "Emergency Kit": True,
    }


@st.cache_data(ttl=600, show_spinner=False)
def get_dashboard_kpis(projects: pd.DataFrame, workers: pd.DataFrame, project_id: str | None = None) -> dict[str, Any]:
    """Compute dashboard KPI values."""
    total = len(projects)
    active = len(projects[projects["Status"] == "Active"])
    completed = len(projects[projects["Status"] == "Completed"])
    avg_progress = projects["Progress"].mean()
    total_budget = projects["Budget"].sum()
    utilized = projects[projects["Status"].isin(["Active", "Delayed"])]["Budget"].sum()
    budget_util = (utilized / total_budget * 100) if total_budget else 0
    present_workers = len(workers[workers["Status"] == "Present"])
    equipment = get_equipment(project_id)
    
    np.random.seed(_get_project_seed(project_id, 49))
    safety_score = round(float(np.random.uniform(88.0, 97.5)), 1)

    return {
        "total_projects": total,
        "active_projects": active,
        "completed_projects": completed,
        "budget_utilization": round(budget_util, 1),
        "workers": present_workers,
        "equipment": len(equipment),
        "safety_score": safety_score,
        "project_completion": round(avg_progress, 1),
    }


@st.cache_data(ttl=600, show_spinner=False)
def get_timeline_data(project_id: str | None = None) -> pd.DataFrame:
    """Generate project timeline chart data."""
    np.random.seed(_get_project_seed(project_id, 47))
    months = pd.date_range("2025-01", periods=18, freq="ME")
    return pd.DataFrame({
        "Month": months.strftime("%b %Y"),
        "Planned": np.cumsum(np.random.randint(3, 8, 18)),
        "Actual": np.cumsum(np.random.randint(2, 7, 18)),
    })


@st.cache_data(ttl=600, show_spinner=False)
def get_budget_allocation(project_id: str | None = None) -> pd.DataFrame:
    """Budget allocation by category."""
    np.random.seed(_get_project_seed(project_id, 50))
    mats = int(np.random.randint(30, 42))
    labor = int(np.random.randint(20, 30))
    eq = int(np.random.randint(12, 18))
    sub = int(np.random.randint(8, 15))
    over = int(np.random.randint(5, 10))
    cont = 100 - (mats + labor + eq + sub + over)
    return pd.DataFrame({
        "Category": ["Materials", "Labor", "Equipment", "Subcontractors", "Overhead", "Contingency"],
        "Amount": [mats, labor, eq, sub, over, max(cont, 3)],
    })


@st.cache_data(ttl=600, show_spinner=False)
def get_project_status_counts(projects: pd.DataFrame) -> pd.DataFrame:
    """Count projects by status."""
    counts = projects["Status"].value_counts().reset_index()
    counts.columns = ["Status", "Count"]
    return counts


@st.cache_data(ttl=600, show_spinner=False)
def get_worker_distribution(workers: pd.DataFrame) -> pd.DataFrame:
    """Worker count by department."""
    return workers.groupby("Department").size().reset_index(name="Count")


@st.cache_data(ttl=600, show_spinner=False)
def get_equipment_usage(project_id: str | None = None) -> pd.DataFrame:
    """Equipment usage hours data."""
    np.random.seed(_get_project_seed(project_id, 51))
    return pd.DataFrame({
        "Equipment": ["Excavator", "Crane", "Bulldozer", "Concrete Mixer", "Dump Truck"],
        "Hours": [int(np.random.randint(800, 1500)) for _ in range(5)],
        "Utilization": [int(np.random.randint(50, 95)) for _ in range(5)],
    })


@st.cache_data(ttl=600, show_spinner=False)
def get_progress_milestones(project_id: str | None = None) -> pd.DataFrame:
    """Project milestones for progress monitoring."""
    np.random.seed(_get_project_seed(project_id, 52))
    p3 = int(np.random.randint(50, 85))
    p4 = int(np.random.randint(15, 50))
    p5 = int(np.random.randint(0, 20))
    return pd.DataFrame([
        {"Milestone": "Site Preparation", "Start": "2026-01-15", "End": "2026-02-28", "Progress": 100, "Status": "Completed"},
        {"Milestone": "Foundation", "Start": "2026-03-01", "End": "2026-05-15", "Progress": 100, "Status": "Completed"},
        {"Milestone": "Structural Frame", "Start": "2026-05-16", "End": "2026-08-30", "Progress": p3, "Status": "In Progress"},
        {"Milestone": "MEP Installation", "Start": "2026-07-01", "End": "2026-10-15", "Progress": p4, "Status": "In Progress"},
        {"Milestone": "Finishing Works", "Start": "2026-09-01", "End": "2026-12-20", "Progress": p5, "Status": "Planning"},
        {"Milestone": "Handover", "Start": "2026-12-21", "End": "2027-01-31", "Progress": 0, "Status": "Planning"},
    ])


@st.cache_data(ttl=600, show_spinner=False)
def get_weekly_progress(project_id: str | None = None) -> pd.DataFrame:
    """Weekly progress percentage data."""
    np.random.seed(_get_project_seed(project_id, 53))
    base = np.sort(np.random.randint(10, 80, 12))
    return pd.DataFrame({
        "Week": [f"W{i}" for i in range(1, 13)],
        "Progress": [int(x) for x in base],
    })


@st.cache_data(ttl=600, show_spinner=False)
def get_monthly_progress(project_id: str | None = None) -> pd.DataFrame:
    """Monthly progress percentage data."""
    np.random.seed(_get_project_seed(project_id, 54))
    act = [int(x) for x in np.sort(np.random.randint(8, 80, 6))]
    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Target": [10, 20, 35, 50, 65, 80],
        "Actual": act,
    })


@st.cache_data(ttl=600, show_spinner=False)
def get_risk_distribution(project_id: str | None = None) -> pd.DataFrame:
    """Safety risk distribution."""
    np.random.seed(_get_project_seed(project_id, 55))
    return pd.DataFrame({
        "Risk Level": ["Low", "Medium", "High", "Critical"],
        "Count": [
            int(np.random.randint(30, 60)),
            int(np.random.randint(15, 35)),
            int(np.random.randint(5, 18)),
            int(np.random.randint(1, 5))
        ],
    })


@st.cache_data(ttl=600, show_spinner=False)
def get_attendance_data(workers: pd.DataFrame, project_id: str | None = None) -> pd.DataFrame:
    """Weekly attendance summary."""
    np.random.seed(_get_project_seed(project_id, 56))
    p = [int(np.random.randint(30, 40)) for _ in range(5)] + [int(np.random.randint(15, 25))]
    a = [40 - x for x in p]
    return pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        "Present": p,
        "Absent": a,
    })

