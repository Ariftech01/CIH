"""Cost estimation module for CIH - Dual Workspace Estimator."""

import io
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import textwrap
import re

from utils import charts
from utils.styles import render_kpi_card, render_page_header
from services.ollamaService import ollama_service
from backend.services.cost_service import cost_service
from backend.schemas.cost_estimation import CostEstimationCreate
from backend.automation.automation_engine import automation_engine

# ==========================================================
# CONSTANTS & ESTIMATION DATA MODELS FOR BASIC & ADVANCED
# ==========================================================

# Basic page constants (legacy rates)
UNIT_RATES = {
    "steel": 68000.0,       # per ton
    "cement": 380.0,        # per bag
    "bricks": 8.5,          # per piece
    "sand": 4500.0,         # per cubic meter
    "labour": 850.0,        # per day
    "machinery": 15000.0,   # per day
    "transportation": 12000.0,  # per trip
}

TAX_RATE = 0.18
CONTINGENCY_RATE = 0.10
MISC_RATE = 0.05

# 19 materials config (Section C)
MATERIALS_CONFIG = [
    {"name": "Cement", "mult": 0.4, "unit": "Bags", "rate": 380.0, "status": "In Stock", "remarks": "Standard PPC cement"},
    {"name": "Steel", "mult": 0.004, "unit": "Tons", "rate": 68000.0, "status": "Ordered", "remarks": "Grade Fe 550 reinforcement"},
    {"name": "Sand", "mult": 0.05, "unit": "Cu.M", "rate": 4500.0, "status": "In Stock", "remarks": "Medium-coarse river sand"},
    {"name": "Bricks", "mult": 12.0, "unit": "Pieces", "rate": 8.5, "status": "In Stock", "remarks": "Class-I clay bricks"},
    {"name": "Concrete", "mult": 0.06, "unit": "Cu.M", "rate": 5500.0, "status": "Scheduled", "remarks": "M25 Ready-Mix Concrete"},
    {"name": "Aggregate", "mult": 0.03, "unit": "Cu.M", "rate": 2200.0, "status": "In Stock", "remarks": "20mm crushed stone"},
    {"name": "Tiles", "mult": 1.1, "unit": "Sq.Ft", "rate": 65.0, "status": "Pending", "remarks": "Vitrified floor tiles"},
    {"name": "Paint", "mult": 0.15, "unit": "Litres", "rate": 280.0, "status": "Pending", "remarks": "Acrylic emulsion paint"},
    {"name": "Wood", "mult": 0.02, "unit": "Cu.Ft", "rate": 1800.0, "status": "Ordered", "remarks": "Teak wood for frames"},
    {"name": "Glass", "mult": 0.08, "unit": "Sq.Ft", "rate": 120.0, "status": "In Stock", "remarks": "5mm clear float glass"},
    {"name": "Doors", "mult": 0.012, "unit": "Units", "rate": 4500.0, "status": "Pending", "remarks": "Flush door shutters"},
    {"name": "Windows", "mult": 0.02, "unit": "Units", "rate": 3200.0, "status": "Pending", "remarks": "UPVC sliding windows"},
    {"name": "Roofing", "mult": 0.15, "unit": "Sq.Ft", "rate": 150.0, "status": "In Stock", "remarks": "GI profile roofing sheets"},
    {"name": "Electrical Materials", "mult": 1.0, "unit": "Lumpsum", "rate": 85.0, "status": "Scheduled", "remarks": "Conduits, wiring & DBs"},
    {"name": "Plumbing Materials", "mult": 1.0, "unit": "Lumpsum", "rate": 75.0, "status": "Scheduled", "remarks": "Pipes, fittings & fixtures"},
    {"name": "Waterproofing", "mult": 0.15, "unit": "Sq.Ft", "rate": 40.0, "status": "Scheduled", "remarks": "Crystalline waterproofing coating"},
    {"name": "Insulation", "mult": 0.10, "unit": "Sq.Ft", "rate": 35.0, "status": "Pending", "remarks": "Glasswool roll insulation"},
    {"name": "Hardware", "mult": 1.0, "unit": "Lumpsum", "rate": 30.0, "status": "In Stock", "remarks": "Hinges, locks & tower bolts"},
    {"name": "Fasteners", "mult": 1.0, "unit": "Lumpsum", "rate": 12.0, "status": "In Stock", "remarks": "Anchor bolts & screws"}
]

# 16 labour roles config (Section D)
LABOUR_CONFIG = [
    {"role": "Project Manager", "req_mult": 1.0, "req_type": "fixed", "wage": 2500.0, "days_mult": 1.0},
    {"role": "Civil Engineer", "req_mult": 0.33, "req_type": "per_floor", "wage": 1800.0, "days_mult": 1.0},
    {"role": "Site Engineer", "req_mult": 0.5, "req_type": "per_floor", "wage": 1500.0, "days_mult": 1.0},
    {"role": "Supervisor", "req_mult": 1.0, "req_type": "per_floor", "wage": 1000.0, "days_mult": 1.0},
    {"role": "Foreman", "req_mult": 0.33, "req_type": "per_floor", "wage": 1200.0, "days_mult": 1.0},
    {"role": "Mason", "req_mult": 0.005, "req_type": "per_sqft", "wage": 850.0, "days_mult": 0.6},
    {"role": "Helper", "req_mult": 0.01, "req_type": "per_sqft", "wage": 500.0, "days_mult": 0.8},
    {"role": "Carpenter", "req_mult": 2.0, "req_type": "fixed", "wage": 800.0, "days_mult": 0.2},
    {"role": "Electrician", "req_mult": 2.0, "req_type": "fixed", "wage": 800.0, "days_mult": 0.15},
    {"role": "Painter", "req_mult": 3.0, "req_type": "fixed", "wage": 750.0, "days_mult": 0.2},
    {"role": "Plumber", "req_mult": 2.0, "req_type": "fixed", "wage": 800.0, "days_mult": 0.15},
    {"role": "Steel Fixer", "req_mult": 2.0, "req_type": "fixed", "wage": 850.0, "days_mult": 0.2},
    {"role": "Welder", "req_mult": 1.0, "req_type": "fixed", "wage": 850.0, "days_mult": 0.1},
    {"role": "Machine Operator", "req_mult": 2.0, "req_type": "fixed", "wage": 1000.0, "days_mult": 0.3},
    {"role": "Cleaner", "req_mult": 2.0, "req_type": "fixed", "wage": 400.0, "days_mult": 1.0},
    {"role": "Security", "req_mult": 2.0, "req_type": "fixed", "wage": 450.0, "days_mult": 1.2}
]

# 11 machinery items config (Section E)
MACHINERY_CONFIG = [
    {"name": "Excavator", "rental": 8000.0, "days_mult": 0.04, "days_min": 5.0, "fuel": 2000.0, "operator": 1000.0, "maintenance": 500.0},
    {"name": "Concrete Mixer", "rental": 2000.0, "days_mult": 0.15, "days_min": 10.0, "fuel": 500.0, "operator": 800.0, "maintenance": 200.0},
    {"name": "Bulldozer", "rental": 12000.0, "days_mult": 0.02, "days_min": 3.0, "fuel": 3000.0, "operator": 1200.0, "maintenance": 600.0},
    {"name": "Crane", "rental": 25000.0, "days_mult": 0.05, "days_min": 3.0, "fuel": 5000.0, "operator": 2000.0, "maintenance": 1000.0},
    {"name": "Concrete Pump", "rental": 15000.0, "days_mult": 0.05, "days_min": 4.0, "fuel": 4000.0, "operator": 1500.0, "maintenance": 800.0},
    {"name": "Loader", "rental": 9000.0, "days_mult": 0.06, "days_min": 5.0, "fuel": 2500.0, "operator": 1000.0, "maintenance": 400.0},
    {"name": "Generator", "rental": 3000.0, "days_mult": 0.5, "days_min": 30.0, "fuel": 1500.0, "operator": 500.0, "maintenance": 200.0},
    {"name": "Compactor", "rental": 1500.0, "days_mult": 0.04, "days_min": 4.0, "fuel": 400.0, "operator": 600.0, "maintenance": 100.0},
    {"name": "Water Tanker", "rental": 2500.0, "days_mult": 0.3, "days_min": 15.0, "fuel": 800.0, "operator": 600.0, "maintenance": 100.0},
    {"name": "Scaffolding", "rental": 500.0, "days_mult": 0.7, "days_min": 30.0, "fuel": 0.0, "operator": 1500.0, "maintenance": 0.0},
    {"name": "Dump Truck", "rental": 7000.0, "days_mult": 0.08, "days_min": 6.0, "fuel": 3000.0, "operator": 800.0, "maintenance": 300.0}
]

# ==========================================================
# HELPER FOR SYNCHRONIZED SLIDER + DIRECT NUMERIC INPUT
# ==========================================================

def _render_slider_number_input(
    label: str,
    min_val: float,
    max_val: float,
    default_val: float,
    step: float,
    key_prefix: str,
    unit: str = ""
) -> float:
    """Render a synchronized Slider + Direct Numeric Input pair."""
    key_val = f"{key_prefix}_val"
    key_slider = f"{key_prefix}_slider"
    key_num = f"{key_prefix}_num"

    if key_val not in st.session_state:
        st.session_state[key_val] = float(default_val)
    if key_slider not in st.session_state:
        st.session_state[key_slider] = float(st.session_state[key_val])
    if key_num not in st.session_state:
        st.session_state[key_num] = float(st.session_state[key_val])

    def _on_slider_change():
        val = float(st.session_state[key_slider])
        st.session_state[key_val] = val
        st.session_state[key_num] = val

    def _on_num_change():
        val = max(float(min_val), min(float(max_val), float(st.session_state[key_num])))
        st.session_state[key_val] = val
        st.session_state[key_slider] = val
        st.session_state[key_num] = val

    unit_str = f" ({unit})" if unit else ""
    col_sl, col_num = st.columns([1.5, 1.0])
    with col_sl:
        st.slider(
            f"{label}{unit_str}",
            min_value=float(min_val),
            max_value=float(max_val),
            step=float(step),
            key=key_slider,
            on_change=_on_slider_change
        )
    with col_num:
        st.number_input(
            f"Exact {label}",
            min_value=float(min_val),
            max_value=float(max_val),
            step=float(step),
            key=key_num,
            on_change=_on_num_change
        )

    return float(st.session_state[key_val])


# ==========================================================
# BASIC PAGE LOGIC FUNCTIONS (Restored verbatim)
# ==========================================================

def _calculate_costs(inputs: dict[str, float]) -> dict[str, float]:
    """Calculate all legacy cost components."""
    material_cost = (
        inputs["steel"] * UNIT_RATES["steel"]
        + inputs["cement"] * UNIT_RATES["cement"]
        + inputs["bricks"] * UNIT_RATES["bricks"]
        + inputs["sand"] * UNIT_RATES["sand"]
    )
    labour_cost = inputs["labour"] * UNIT_RATES["labour"]
    machinery_cost = inputs["machinery"] * UNIT_RATES["machinery"]
    transport_cost = inputs["transportation"] * UNIT_RATES["transportation"]

    subtotal = material_cost + labour_cost + machinery_cost + transport_cost
    tax = subtotal * TAX_RATE
    contingency = subtotal * CONTINGENCY_RATE
    grand_total = subtotal + tax + contingency

    return {
        "material_cost": material_cost,
        "labour_cost": labour_cost + machinery_cost + transport_cost,
        "tax": tax,
        "contingency": contingency,
        "grand_total": grand_total,
        "subtotal": subtotal,
    }

def _format_inr(amount: float) -> str:
    """Format amount in Indian Rupees."""
    return f"₹{amount:,.2f}"

# ==========================================================
# ADVANCED PAGE LOGIC FUNCTIONS
# ==========================================================

def calculate_advanced_estimates(built_up_area: float, timeline_days: float, num_floors: float):
    """Estimate material, labour, and machinery requirements dynamically."""
    
    # 1. Materials List (19 items)
    mat_rows = []
    total_mat_cost = 0.0
    for m in MATERIALS_CONFIG:
        qty = built_up_area * m["mult"]
        cost = qty * m["rate"]
        total_mat_cost += cost
        mat_rows.append({
            "Material Name": m["name"],
            "Quantity": round(qty, 1),
            "Unit": m["unit"],
            "Approximate Rate": m["rate"],
            "Estimated Cost": round(cost, 2),
            "Status": m["status"],
            "Remarks": m["remarks"]
        })
    mat_df = pd.DataFrame(mat_rows)

    # 2. Labour Requirements (16 roles)
    lab_rows = []
    total_lab_cost = 0.0
    for l in LABOUR_CONFIG:
        if l["req_type"] == "fixed":
            workers = l["req_mult"]
        elif l["req_type"] == "per_floor":
            workers = max(1.0, float(num_floors) * l["req_mult"])
        elif l["req_type"] == "per_sqft":
            workers = max(1.0, float(built_up_area) * l["req_mult"])
        else:
            workers = 1.0

        workers = int(round(workers))
        days = max(5.0, float(timeline_days) * l["days_mult"])
        days = int(round(days))
        cost = workers * l["wage"] * days
        total_lab_cost += cost
        lab_rows.append({
            "Role": l["role"],
            "Workers Required": workers,
            "Estimated Working Days": days,
            "Daily Wage": l["wage"],
            "Estimated Cost": round(cost, 2)
        })
    lab_df = pd.DataFrame(lab_rows)

    # 3. Machinery Sizing (11 items)
    mach_rows = []
    total_mach_cost = 0.0
    for m in MACHINERY_CONFIG:
        days = max(m["days_min"], float(timeline_days) * m["days_mult"])
        days = int(round(days))

        rental_total = m["rental"] * days
        fuel_total = m["fuel"] * days
        operator_total = m["operator"] * days
        maint_total = m["maintenance"] * days

        row_cost = rental_total + fuel_total + operator_total + maint_total
        total_mach_cost += row_cost
        mach_rows.append({
            "Machine Name": m["name"],
            "Rental Cost": m["rental"],
            "Estimated Days": days,
            "Fuel Cost": m["fuel"],
            "Operator Cost": m["operator"],
            "Maintenance Cost": m["maintenance"],
            "Estimated Cost": round(row_cost, 2)
        })
    mach_df = pd.DataFrame(mach_rows)

    return mat_df, lab_df, mach_df, total_mat_cost, total_lab_cost, total_mach_cost

# ==========================================================
# FLOOR CONFIGURATION ACTION LOGIC
# ==========================================================

def adv_add_floor():
    floor_num = len(st.session_state.adv_floors) + 1
    st.session_state.adv_floors.append({
        "name": f"Floor {floor_num}",
        "rooms": [{"name": "Living Room", "type": "Hall", "length": 16.0, "width": 14.0, "height": 10.0}]
    })

def adv_delete_floor(idx):
    if len(st.session_state.adv_floors) > 1:
        st.session_state.adv_floors.pop(idx)
    else:
        st.warning("⚠️ At least one floor must remain in the building structure.")

def adv_add_room(floor_idx):
    rooms = st.session_state.adv_floors[floor_idx]["rooms"]
    rooms.append({
        "name": f"Room {len(rooms) + 1}",
        "type": "Bedroom",
        "length": 12.0,
        "width": 10.0,
        "height": 10.0
    })

def adv_delete_room(floor_idx, room_idx):
    rooms = st.session_state.adv_floors[floor_idx]["rooms"]
    if len(rooms) > 1:
        rooms.pop(room_idx)
    else:
        st.warning("⚠️ At least one room must remain on a floor.")

def adv_duplicate_room(floor_idx, room_idx):
    rooms = st.session_state.adv_floors[floor_idx]["rooms"]
    original = rooms[room_idx]
    rooms.append({
        "name": f"{original['name']} (Copy)",
        "type": original["type"],
        "length": original["length"],
        "width": original["width"],
        "height": original.get("height", 10.0)
    })

# ==========================================================
# AI OFFLINE SIMULATED CONSULTANT
# ==========================================================

def generate_python_simulated_response(prompt: str, context_str: str) -> str:
    p = prompt.lower()
    
    # Helper to parse context
    def get_val(pattern, default="N/A"):
        match = re.search(pattern, context_str)
        return match.group(1).strip() if match else default

    proj_name = get_val(r"Project Name:\s*(.*)")
    proj_type = get_val(r"Construction Type:\s*(.*)")
    built_area = get_val(r"Built-up Area:\s*(.*)")
    duration = get_val(r"Timeline:\s*(.*)")
    grand_total = get_val(r"Grand Total:\s*(.*)")
    cost_per_sqft = get_val(r"Estimated Cost per Sq Ft:\s*(.*)")
    
    # Pre-calculate BOQ cell values to avoid backslashes inside f-string interpolation braces
    mat_cost_val = get_val(r"Material Cost:\s*(.*)")
    lab_cost_val = get_val(r"Labour Cost:\s*(.*)")
    mach_cost_val = get_val(r"Machinery Cost:\s*(.*)")
    trans_cost_val = get_val(r"Transportation Cost:\s*(.*)")
    tax_cost_val = get_val(r"Tax Cost:\s*(.*)")
    contingency_cost_val = get_val(r"Contingency Cost:\s*(.*)")
    misc_cost_val = get_val(r"Miscellaneous Cost:\s*(.*)")
    
    # Pre-calculate BOQ details
    qty_cement = get_val(r"- Cement: Qty=(.*?)\s")
    cost_cement = get_val(r"- Cement: Qty=.*?Cost=(.*?)\s")
    qty_steel = get_val(r"- Steel: Qty=(.*?)\s")
    cost_steel = get_val(r"- Steel: Qty=.*?Cost=(.*?)\s")
    qty_sand = get_val(r"- Sand: Qty=(.*?)\s")
    cost_sand = get_val(r"- Sand: Qty=.*?Cost=(.*?)\s")
    qty_concrete = get_val(r"- Concrete: Qty=(.*?)\s")
    cost_concrete = get_val(r"- Concrete: Qty=.*?Cost=(.*?)\s")
    qty_bricks = get_val(r"- Bricks: Qty=(.*?)\s")
    cost_bricks = get_val(r"- Bricks: Qty=.*?Cost=(.*?)\s")

    reply = "### 🤖 [Offline Simulation] AI Construction Advisor\n\n"
    
    if "boq" in p or "bill of quantities" in p:
        reply += f"""Here is the **Bill of Quantities (BOQ)** summary compiled for **{proj_name}** based on the current workspace estimations:

| Component Category | Description | Estimated Cost |
| :--- | :--- | :--- |
| **Material Costs** | Structural steel, cement, sand, concrete, finish materials | {mat_cost_val} |
| **Labour Costs** | Site crew, engineers, supervisors, masons, and assistants | {lab_cost_val} |
| **Machinery Costs** | Heavy vehicle rental, operator hire, and maintenance | {mach_cost_val} |
| **Transportation** | Logistics, JIT concrete transit, material transport | {trans_cost_val} |
| **Overheads & Taxes** | 18% GST Compliance | {tax_cost_val} |
| **Contingency Reserves** | 10% Risk hedge margin | {contingency_cost_val} |
| **Miscellaneous** | Site utilities and administrative overheads | {misc_cost_val} |
| **Grand Total Project Estimate** | **Calculated BOQ sum** | **{grand_total}** |

*Estimated Cost per Square Foot: **{cost_per_sqft}***"""
    elif "reduce" in p or "cheaper" in p or "saving" in p or "save" in p:
        reply += f"""Based on the current estimated project cost of **{grand_total}** for your **{proj_type}** building, here are target saving strategies:
1. **Material Alternatives**: Use *Fly Ash Bricks* or AAC Blocks instead of standard clay bricks. This can shave up to 15% off masonry work.
2. **Cement Optimization**: Utilize *Portland Pozzolana Cement (PPC)* for brickwork and plastering. It is cheaper and more durable for non-structural applications.
3. **Labour Logistics**: Limit specialized trades to critical-path phases. Ensure helper-to-mason ratios are locked at 1.5:1.
4. **Machinery Hire**: Optimize Concrete Pump rental days. Batch pouring phases together to minimize daily standby charges.
5. **Fasteners & Consumables**: Purchase fasteners and hardware accessories in bulk direct from wholesale vendors to achieve a 10% saving."""
    elif "alternative" in p:
        reply += f"""### Alternative Construction Methods & Material Optimization
For the **{built_area}** structure, we recommend evaluating the following alternative methods:
1. **Precast RCC Elements**: Consider using precast slabs or beams. It increases speed by 30% and reduces on-site helper costs significantly.
2. **Glass & Wood Alternatives**: Substitute teak doors with pre-finished composite doors, and use UPVC window framing instead of aluminium for superior energy efficiency and a 20% lower cost.
3. **Aggregates**: Check availability of recycled aggregates for sub-bases or landscaping concrete, saving up to ₹500 per cu.m.
4. **Waterproofing Membrane**: Use bituminous self-adhesive membrane instead of liquid coating for roofing areas for longer life and shorter labor application times."""
    elif "labour" in p or "labor" in p:
        reply += f"""### Labour Requirements & Sizing Optimization
The current labour cost is estimated at **{lab_cost_val}**.
- **Crew Allocation**: Masons, Helpers, and Supervisors are sized according to productivity output norms over the **{duration}** schedule.
- **Optimization Strategy**: We recommend setting site progress milestones. Ensure specialized roles (like Welder, Painter, Plumber) are scheduled back-to-back to prevent idle daily wages (ranging from ₹750 to ₹850/day)."""
    elif "machinery" in p or "machine" in p:
        reply += f"""### Machinery Deployment Assessment
The total estimated machinery expenditure is **{mach_cost_val}**.
- **Critical Path Machines**: Crane (rental ₹25,000/day) and Excavator (rental ₹8,000/day) are cost-drivers.
- **Deployment Tip**: Schedule deep excavation strictly in the first 15 days to return the Excavator early. Keep Scaffolding on a monthly hire contract rather than daily, which saves up to 30%."""
    elif "timeline" in p or "schedule" in p:
        reply += f"""### Timeline Optimization Schedule
For a project duration of **{duration}**, we recommend the following timeline structure:
- **Phase 1 (Site Prep & Foundation)**: Days 1 - 45 (Excavator, Bulldozer, Compactor)
- **Phase 2 (Superstructure RCC Slabs)**: Days 46 - 200 (Crane, Concrete Pump, Mixer)
- **Phase 3 (Brickwork & Finishes)**: Days 201 - 320 (Masons, Helpers, Carpenters)
- **Phase 4 (MEP Services & Testing)**: Days 321 - 400 (Plumbers, Electricians)
- **Phase 5 (Finishing & Cleaning)**: Days 401 - {duration}"""
    elif "risk" in p:
        # Avoid backslash in float cast
        dur_clean = duration.replace('Days','').strip()
        dur_val = int(float(dur_clean)*0.1) if dur_clean.replace('.','',1).isdigit() else 45
        reply += f"""### Risk Analysis Report
1. **Price Escalation Risk**: Steel (₹68,000/ton) and Cement (₹380/bag) are highly volatile. Hedge this risk by procuring 40% of material requirements in bulk at start.
2. **Weather Risk**: Curing RCC works during peak summer requires water tankers. Dewatering pumps must be present during monsoons to avoid basement flooding.
3. **Timeline Drift**: High-rise crane operations are affected by high wind speeds. Budget a 10% contingency day buffer (approx. {dur_val} days)."""
    elif "boq" in p or "quantities" in p or "material" in p:
        reply += f"""### Basic Bill of Quantities (BOQ) Summary
Project: **{proj_name}**
Built-up Area: **{built_area}**

| Item Description | Unit | Quantity | Approx Rate | Estimated Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Cement** | Bags | {qty_cement} | ₹380 | {cost_cement} |
| **Steel** | Tons | {qty_steel} | ₹68,000 | {cost_steel} |
| **Sand** | Cu.M | {qty_sand} | ₹4,500 | {cost_sand} |
| **Concrete** | Cu.M | {qty_concrete} | ₹5,500 | {cost_concrete} |
| **Bricks** | Pieces | {qty_bricks} | ₹8.5 | {cost_bricks} |
| **Labour Force** | Lumpsum | - | - | {lab_cost_val} |
| **Machinery & Fleet** | Lumpsum | - | - | {mach_cost_val} |

*This BOQ is a preliminary estimate. Detailed structural drawings are required for execution BOQs.*"""
    else:
        reply += f"""I have analyzed the **{proj_name}** project details.
- **Estimated Grand Total**: {grand_total} (approx. {cost_per_sqft} per sq ft)
- **Built-up Area**: {built_area}
- **Construction Type**: {proj_type}

How can I help you with BOQs, cost reductions, material alternatives, labor sufficiency, or risk reports?"""
        
    return reply

# ==========================================================
# EXPORT DOCUMENTS LOGIC V2
# ==========================================================

def generate_excel_bytes_v2(proj_info, mat_df, lab_df, mach_df, summary_costs):
    """Construct multi-sheet Excel workbooks with styling."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        meta_data = []
        for key, val in proj_info.items():
            meta_data.append({"Information Parameter": key, "Value Details": str(val)})
        meta_data.append({"Information Parameter": "", "Value Details": ""})
        meta_data.append({"Information Parameter": "=== COST ACCOUNT SUMMARY ===", "Value Details": ""})
        for key, val in summary_costs.items():
            meta_data.append({"Information Parameter": key, "Value Details": _format_inr(val) if isinstance(val, (int, float)) else str(val)})
        
        pd.DataFrame(meta_data).to_excel(writer, sheet_name="Project summary", index=False)
        mat_df.to_excel(writer, sheet_name="Materials sheet", index=False)
        lab_df.to_excel(writer, sheet_name="Labour schedule", index=False)
        mach_df.to_excel(writer, sheet_name="Equipment list", index=False)
        
    return output.getvalue()

def compile_adv_context_v2(proj_details, floors_data, mat_df, lab_df, mach_df, cost_summary):
    # Compiles everything into a clean markdown format
    lines = []
    lines.append("=== SYSTEM CONTEXT (CONSTRUCTION ESTIMATOR) ===")
    lines.append(f"Project Name: {proj_details['name']}")
    lines.append(f"Project ID: {proj_details['id']}")
    lines.append(f"Client: {proj_details['client']}")
    lines.append(f"Location: {proj_details['location']}")
    lines.append(f"Construction Type: {proj_details['type']}")
    lines.append(f"Category: {proj_details['category']}")
    lines.append(f"Floors: {proj_details['floors']}")
    lines.append(f"Timeline: {proj_details['timeline']} Days")
    lines.append(f"Built-up Area: {proj_details['built_up_area']:.1f} sqft")
    
    lines.append("\n=== BUILDING STRUCTURE ===")
    for f_idx, f in enumerate(floors_data):
        lines.append(f"- Floor {f_idx + 1}: {f['name']}")
        for r in f["rooms"]:
            lines.append(f"  * {r['name']} ({r['type']}): {r['length']}x{r['width']} ft, H={r['height']} ft, Area={r['length']*r['width']:.1f} sqft")
            
    lines.append("\n=== MATERIAL ESTIMATES ===")
    for _, r in mat_df.iterrows():
        lines.append(f"- {r['Material Name']}: Qty={r['Quantity']:,} {r['Unit']}, Rate=₹{r['Approximate Rate']:,}, Cost=₹{r['Estimated Cost']:,}, Status={r['Status']}, Remarks={r['Remarks']}")
        
    lines.append("\n=== LABOUR REQUIREMENTS ===")
    for _, r in lab_df.iterrows():
        lines.append(f"- {r['Role']}: Workers={r['Workers Required']}, Days={r['Estimated Working Days']}, Wage=₹{r['Daily Wage']}, Cost=₹{r['Estimated Cost']:,}")
        
    lines.append("\n=== MACHINERY REQUIREMENTS ===")
    for _, r in mach_df.iterrows():
        lines.append(f"- {r['Machine Name']}: Rental=₹{r['Rental Cost']}/day, Days={r['Estimated Days']}, Fuel=₹{r['Fuel Cost']}/day, Op=₹{r['Operator Cost']}/day, Maint=₹{r['Maintenance Cost']}/day")
        
    lines.append("\n=== COST BREAKDOWN ===")
    for k, v in cost_summary.items():
        lines.append(f"- {k}: {v}")
        
    return "\n".join(lines)

# ==========================================================
# RENDER DISPATCHER
# ==========================================================

def render() -> None:
    """Render cost estimation navigation portal."""
    
    # Render two top-level navigation tabs
    tab_basic, tab_construction = st.tabs(["Basic Cost Estimation", "Construction Estimator"])

    # ------------------------------------------------------
    # TAB 1: BASIC COST ESTIMATION (Restored verbatim)
    # ------------------------------------------------------
    with tab_basic:
        # Script block to ensure the global floating assistant widget is shown
        st.markdown(
            """
            <script>
            (function() {
                const hostDoc = window.parent.document || document;
                const rootNode = hostDoc.getElementById("cih-assistant-root");
                if (rootNode) {
                    rootNode.style.display = "block";
                }
            })();
            </script>
            """,
            unsafe_allow_html=True
        )

        render_page_header("Cost Estimation", "Enterprise-grade construction cost calculator")

        col_input, col_output = st.columns([1, 1])

        with col_input:
            st.markdown(
                """
                <div class="cih-glass-card">
                    <div class="cih-card-title">📝 Cost Input Parameters</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("**Materials (Slider + Exact Input)**")
            steel = _render_slider_number_input("Steel", 0.0, 500.0, 50.0, 0.5, "basic_steel", "Tons")
            cement = _render_slider_number_input("Cement", 0.0, 20000.0, 2000.0, 10.0, "basic_cement", "Bags")
            bricks = _render_slider_number_input("Bricks", 0.0, 500000.0, 50000.0, 100.0, "basic_bricks", "Units")
            sand = _render_slider_number_input("Sand", 0.0, 2000.0, 150.0, 1.0, "basic_sand", "Cu.M")

            st.markdown("**Resources (Slider + Exact Input)**")
            labour = _render_slider_number_input("Labour", 0.0, 1000.0, 120.0, 1.0, "basic_labour", "Days")
            machinery = _render_slider_number_input("Machinery", 0.0, 500.0, 45.0, 1.0, "basic_machinery", "Days")
            transportation = _render_slider_number_input("Transportation", 0.0, 300.0, 30.0, 1.0, "basic_transportation", "Trips")

            calculate = st.button("🔢 Calculate Estimate", use_container_width=True, type="primary", key="basic_calc")

        inputs = {
            "steel": steel, "cement": cement, "bricks": bricks, "sand": sand,
            "labour": labour, "machinery": machinery, "transportation": transportation,
        }
        costs = _calculate_costs(inputs)

        with col_output:
            st.markdown(
                """
                <div class="cih-glass-card">
                    <div class="cih-card-title">💰 Cost Summary</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            summary_cols = st.columns(2)
            with summary_cols[0]:
                render_kpi_card("Material Cost", _format_inr(costs["material_cost"]), "🧱")
            with summary_cols[1]:
                render_kpi_card("Labour & Ops", _format_inr(costs["labour_cost"]), "👷")

            summary_cols2 = st.columns(2)
            with summary_cols2[0]:
                render_kpi_card("Tax (18% GST)", _format_inr(costs["tax"]), "📋")
            with summary_cols2[1]:
                render_kpi_card("Contingency (10%)", _format_inr(costs["contingency"]), "🛡️")

            st.markdown(
                f"""
                <div class="cih-kpi-card" style="text-align:center; margin-top:1rem; animation: pulseGlow 2s infinite;">
                    <div class="cih-kpi-label">Grand Total</div>
                    <div class="cih-kpi-value" style="font-size:2.5rem; color:#3B82F6;">{_format_inr(costs['grand_total'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if calculate:
                st.success("✅ Cost estimate calculated successfully!")

        st.markdown("<br>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig = charts.create_cost_breakdown_chart(
                costs["material_cost"], costs["labour_cost"], costs["tax"], costs["contingency"],
            )
            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            st.markdown(
                f"""
                <div class="cih-glass-card">
                    <div class="cih-card-title">📊 Rate Reference</div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Steel</span><span class="cih-metric-value">₹68,000/ton</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Cement</span><span class="cih-metric-value">₹380/bag</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Bricks</span><span class="cih-metric-value">₹8.5/unit</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Sand</span><span class="cih-metric-value">₹4,500/cu.m</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Labour</span><span class="cih-metric-value">₹850/day</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Machinery</span><span class="cih-metric-value">₹15,000/day</span></div>
                    <div class="cih-metric-row"><span class="cih-metric-label">Transport</span><span class="cih-metric-value">₹12,000/trip</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ------------------------------------------------------
    # TAB 2: CONSTRUCTION ESTIMATOR (Section A-H Advanced Page)
    # ------------------------------------------------------
    with tab_construction:
        # Script block to ensure the global floating assistant widget is hidden
        st.markdown(
            """
            <script>
            (function() {
                const hostDoc = window.parent.document || document;
                const rootNode = hostDoc.getElementById("cih-assistant-root");
                if (rootNode) {
                    rootNode.style.display = "none";
                }
            })();
            </script>
            """,
            unsafe_allow_html=True
        )

        # Injected styles for advanced estimator workspace
        st.markdown(
            """
            <style>
            .adv-workspace-title {
                font-family: 'Outfit', sans-serif;
                font-weight: 700;
                color: #FFFFFF;
                font-size: 1.6rem;
                margin-bottom: 0.5rem;
            }
            .adv-glass-container {
                background: rgba(15, 23, 42, 0.45);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px;
                padding: 1.25rem;
                margin-bottom: 1.5rem;
            }
            .adv-table-wrapper {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 20px;
                overflow-x: auto;
            }
            .adv-custom-table {
                width: 100%;
                border-collapse: collapse;
                color: #E2E8F0;
                font-size: 0.85rem;
            }
            .adv-custom-table th {
                background: rgba(255, 255, 255, 0.04);
                border-bottom: 2px solid rgba(255, 255, 255, 0.08);
                color: #94A3B8;
                text-align: left;
                padding: 10px 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.03em;
            }
            .adv-custom-table td {
                padding: 10px 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            }
            .adv-custom-table tr:hover {
                background: rgba(255, 255, 255, 0.015);
            }
            .adv-custom-table tr:last-child td {
                border-bottom: none;
            }
            .adv-status-badge {
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 0.72rem;
                font-weight: 600;
            }
            .adv-status-instock { background: rgba(34, 197, 94, 0.15); color: #4ADE80; border: 1px solid rgba(34, 197, 94, 0.25); }
            .adv-status-ordered { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.25); }
            .adv-status-scheduled { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.25); }
            .adv-status-pending { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.25); }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Initialize State Variables
        if "adv_project_name" not in st.session_state:
            st.session_state.adv_project_name = "Downtown Plaza Tower A"
        if "adv_project_id" not in st.session_state:
            st.session_state.adv_project_id = "PRJ-2026-DPTA"
        if "adv_client_name" not in st.session_state:
            st.session_state.adv_client_name = "Vertex Holdings Group"
        if "adv_project_location" not in st.session_state:
            st.session_state.adv_project_location = "Sector 62, Noida, India"
        if "adv_construction_type" not in st.session_state:
            st.session_state.adv_construction_type = "Commercial"
        if "adv_building_category" not in st.session_state:
            st.session_state.adv_building_category = "High Rise"
        if "adv_num_floors" not in st.session_state:
            st.session_state.adv_num_floors = 12
        if "adv_duration_days" not in st.session_state:
            st.session_state.adv_duration_days = 540
        if "adv_plot_area" not in st.session_state:
            st.session_state.adv_plot_area = 15000.0
        if "adv_built_up_area" not in st.session_state:
            st.session_state.adv_built_up_area = 120000.0
        if "adv_budget_limit" not in st.session_state:
            st.session_state.adv_budget_limit = 150000000.0
        if "adv_chat_history" not in st.session_state:
            st.session_state.adv_chat_history = [
                {
                    "role": "assistant",
                    "content": "Welcome to your embedded Construction Estimator AI Advisor. I have parsed your active building layouts, material totals, and machinery rental schedule. Ask me any queries about cost-savings, timelines, or BOQs!"
                }
            ]
        if "adv_floors" not in st.session_state:
            st.session_state.adv_floors = [
                {
                    "name": "Ground Floor",
                    "rooms": [
                        {"name": "Reception Lobby", "type": "Custom", "length": 30.0, "width": 20.0, "height": 12.0},
                        {"name": "Manager Office", "type": "Office", "length": 15.0, "width": 12.0, "height": 10.0},
                        {"name": "Conference Room", "type": "Custom", "length": 25.0, "width": 15.0, "height": 10.0},
                        {"name": "Cafeteria", "type": "Dining", "length": 20.0, "width": 15.0, "height": 10.0},
                        {"name": "Restroom A", "type": "Bathroom", "length": 10.0, "width": 8.0, "height": 10.0},
                    ]
                },
                {
                    "name": "First Floor",
                    "rooms": [
                        {"name": "Open Workstation", "type": "Office", "length": 40.0, "width": 25.0, "height": 10.0},
                        {"name": "Pantry Room", "type": "Kitchen", "length": 12.0, "width": 10.0, "height": 10.0},
                        {"name": "Restroom B", "type": "Bathroom", "length": 10.0, "width": 8.0, "height": 10.0},
                        {"name": "Server Room", "type": "Store", "length": 15.0, "width": 10.0, "height": 10.0},
                    ]
                }
            ]

        # Division of Layout into Workspace and AI Advisor Column
        col_workspace, col_ai = st.columns([2.1, 1.0])

        with col_workspace:
            st.markdown('<div class="adv-workspace-title">🏗️ Enterprise Construction Estimator</div>', unsafe_allow_html=True)
            st.markdown("<p style='color:#64748B; margin-top:-5px; font-size:0.85rem; margin-bottom:15px;'>Professional workspace for structural configs, detailed estimations, and documentation exports.</p>", unsafe_allow_html=True)

            # ------------------------------------------------------
            # SECTION A: PROJECT DETAILS
            # ------------------------------------------------------
            with st.container():
                st.markdown(
                    """
                    <div class="cih-glass-card">
                        <div class="cih-card-title">📝 Project Profiling (Section A)</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                ap_name = st.text_input("Project Name", value=st.session_state.adv_project_name, key="adv_pname_in")
                st.session_state.adv_project_name = ap_name

                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    ap_id = st.text_input("Project ID", value=st.session_state.adv_project_id, key="adv_pid_in")
                    st.session_state.adv_project_id = ap_id
                    a_client = st.text_input("Client", value=st.session_state.adv_client_name, key="adv_client_in")
                    st.session_state.adv_client_name = a_client
                    a_budget = st.number_input("Budget Limit (₹)", min_value=0.0, value=st.session_state.adv_budget_limit, step=1000000.0, key="adv_budget_in")
                    st.session_state.adv_budget_limit = a_budget
                with col_a2:
                    ap_loc = st.text_input("Location", value=st.session_state.adv_project_location, key="adv_loc_in")
                    st.session_state.adv_project_location = ap_loc
                    a_duration = st.number_input("Expected Timeline (Days)", min_value=10, value=int(st.session_state.adv_duration_days), step=5, key="adv_duration_in")
                    st.session_state.adv_duration_days = a_duration
                    a_plot = st.number_input("Total Plot Area (sq ft)", min_value=10.0, value=float(st.session_state.adv_plot_area), step=100.0, key="adv_plot_in")
                    st.session_state.adv_plot_area = a_plot

                col_a3, col_a4 = st.columns(2)
                with col_a3:
                    adv_c_types = ["Residential", "Commercial", "Industrial", "Hospital", "Apartment", "Villa", "School"]
                    adv_c_idx = adv_c_types.index(st.session_state.adv_construction_type) if st.session_state.adv_construction_type in adv_c_types else 0
                    ap_type = st.selectbox("Construction Type", adv_c_types, index=adv_c_idx, key="adv_type_sel")
                    st.session_state.adv_construction_type = ap_type
                with col_a4:
                    adv_b_cats = ["Single Floor", "Duplex", "Multi Floor", "High Rise"]
                    adv_b_idx = adv_b_cats.index(st.session_state.adv_building_category) if st.session_state.adv_building_category in adv_b_cats else 0
                    ap_cat = st.selectbox("Building Category", adv_b_cats, index=adv_b_idx, key="adv_cat_sel")
                    st.session_state.adv_building_category = ap_cat

                ap_floors = st.number_input("Number of Floors", min_value=1, value=int(st.session_state.adv_num_floors), step=1, key="adv_floors_in")
                st.session_state.adv_num_floors = ap_floors

            # ------------------------------------------------------
            # SECTION B: FLOOR BUILDER
            # ------------------------------------------------------
            st.markdown(
                """
                <div class="cih-glass-card">
                    <div class="cih-card-title">🏢 Floor & Room Configurator (Section B)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Compute dynamic area values
            building_area = 0.0
            for f_idx, floor in enumerate(st.session_state.adv_floors):
                fl_area = sum(r["length"] * r["width"] for r in floor["rooms"])
                building_area += fl_area

            # Update built-up area
            st.session_state.adv_built_up_area = building_area

            st.write(f"**Total Floors Structured: {len(st.session_state.adv_floors)} | Total Built-up Area: {building_area:,.2f} sq ft**")

            for f_idx, floor in enumerate(st.session_state.adv_floors):
                fl_area = sum(r["length"] * r["width"] for r in floor["rooms"])
                
                with st.expander(f"🏢 {floor['name']} — (Area: {fl_area:,.1f} sq ft)", expanded=(f_idx == 0)):
                    new_fname = st.text_input("Floor Title", value=floor["name"], key=f"adv_fname_{f_idx}")
                    if new_fname != floor["name"]:
                        floor["name"] = new_fname
                        st.rerun()

                    rooms = floor["rooms"]
                    for r_idx, room in enumerate(rooms):
                        st.markdown(f"**Room #{r_idx + 1}**")
                        cf_type, cf_name, cf_len, cf_wid, cf_hei, cf_area, cf_act = st.columns([1.8, 1.8, 1.0, 1.0, 1.0, 1.2, 1.2])
                        
                        with cf_type:
                            adv_r_types = ["Bedroom", "Kitchen", "Hall", "Dining", "Bathroom", "Office", "Garage", "Balcony", "Study", "Store", "Utility", "Custom"]
                            r_idx_t = adv_r_types.index(room["type"]) if room["type"] in adv_r_types else 0
                            sel_type = st.selectbox("Type", adv_r_types, index=r_idx_t, key=f"adv_r_type_{f_idx}_{r_idx}")
                            room["type"] = sel_type
                        with cf_name:
                            val_name = st.text_input("Name", value=room["name"], key=f"adv_r_name_{f_idx}_{r_idx}")
                            room["name"] = val_name
                        with cf_len:
                            val_len = st.number_input("L (ft)", min_value=1.0, value=float(room["length"]), step=0.5, key=f"adv_r_len_{f_idx}_{r_idx}")
                            room["length"] = val_len
                        with cf_wid:
                            val_wid = st.number_input("W (ft)", min_value=1.0, value=float(room["width"]), step=0.5, key=f"adv_r_wid_{f_idx}_{r_idx}")
                            room["width"] = val_wid
                        with cf_hei:
                            val_hei = st.number_input("H (ft)", min_value=0.0, value=float(room.get("height", 10.0)), step=0.5, key=f"adv_r_hei_{f_idx}_{r_idx}")
                            room["height"] = val_hei
                        with cf_area:
                            area_val = val_len * val_wid
                            st.markdown(f"<div style='margin-top:28px; font-weight:600; color:#10B981;'>{area_val:.1f} sqft</div>", unsafe_allow_html=True)
                        with cf_act:
                            st.write("")
                            st.write("")
                            cad1, cad2 = st.columns(2)
                            with cad1:
                                if st.button("👥", key=f"adv_r_dup_{f_idx}_{r_idx}", help="Duplicate"):
                                    adv_duplicate_room(f_idx, r_idx)
                                    st.rerun()
                            with cad2:
                                if st.button("🗑️", key=f"adv_r_del_{f_idx}_{r_idx}", help="Delete"):
                                    adv_delete_room(f_idx, r_idx)
                                    st.rerun()
                                    
                    st.write("")
                    col_fl_act1, col_fl_act2 = st.columns(2)
                    with col_fl_act1:
                        if st.button(f"➕ Add Room to {floor['name']}", key=f"adv_add_room_{f_idx}"):
                            adv_add_room(f_idx)
                            st.rerun()
                    with col_fl_act2:
                        if len(st.session_state.adv_floors) > 1:
                            if st.button(f"🗑️ Delete Floor {floor['name']}", key=f"adv_del_floor_{f_idx}", type="secondary"):
                                adv_delete_floor(f_idx)
                                st.rerun()

            if st.button("➕ Add Floor Block", key="adv_add_floor_block", type="primary"):
                adv_add_floor()
                st.rerun()

            # Pre-calculate advanced estimates based on dynamic inputs
            mat_df, lab_df, mach_df, adv_mat_total, adv_lab_total, adv_mach_total = calculate_advanced_estimates(
                st.session_state.adv_built_up_area, st.session_state.adv_duration_days, st.session_state.adv_num_floors
            )

            # Logistics Transport cost
            adv_trans_cost = max(10.0, st.session_state.adv_built_up_area * 0.00025) * 12000.0

            # ------------------------------------------------------
            # SECTION C: AUTOMATIC MATERIAL ESTIMATION
            # ------------------------------------------------------
            st.write("### 🧱 Material Estimation Table (Section C)")

            # Interactive Slider + Direct Numeric Input Adjuster for 19 Materials
            with st.expander("🎛️ Interactive Material Multipliers & Rates Adjuster (19 Materials)", expanded=False):
                st.caption("Adjust exact quantities or rates using synchronized Sliders + Direct Numeric Inputs:")
                for idx, m in enumerate(MATERIALS_CONFIG):
                    default_qty = round(st.session_state.adv_built_up_area * m["mult"], 1)
                    max_qty = max(default_qty * 3.0, 100.0)
                    step_val = 0.5 if default_qty < 100 else 1.0 if default_qty < 1000 else 10.0
                    
                    adjusted_qty = _render_slider_number_input(
                        m["name"],
                        0.0,
                        max_qty,
                        default_qty,
                        step_val,
                        f"adv_mat_input_{idx}",
                        m["unit"]
                    )
                    # Override calculated quantity for mat_df row
                    if idx < len(mat_df):
                        mat_df.at[idx, "Quantity"] = adjusted_qty
                        mat_df.at[idx, "Estimated Cost"] = round(adjusted_qty * m["rate"], 2)

                adv_mat_total = mat_df["Estimated Cost"].sum()

            mat_rows_list = []
            for _, r in mat_df.iterrows():
                badge_class = "adv-status-instock"
                if r["Status"] == "Ordered": badge_class = "adv-status-ordered"
                elif r["Status"] == "Scheduled": badge_class = "adv-status-scheduled"
                elif r["Status"] == "Pending": badge_class = "adv-status-pending"

                mat_rows_list.append(
                    f"<tr><td>{r['Material Name']}</td><td>{r['Quantity']:,.1f}</td><td>{r['Unit']}</td><td>₹{r['Approximate Rate']:,.1f}</td><td>₹{r['Estimated Cost']:,.1f}</td><td><span class='adv-status-badge {badge_class}'>{r['Status']}</span></td><td>{r['Remarks']}</td></tr>"
                )
            mat_rows_html = "".join(mat_rows_list)

            st.markdown(
                f"""
                <div class="adv-table-wrapper">
                    <table class="adv-custom-table">
                        <thead>
                            <tr>
                                <th>Material Name</th>
                                <th>Quantity</th>
                                <th>Unit</th>
                                <th>Approx. Rate</th>
                                <th>Estimated Cost</th>
                                <th>Status</th>
                                <th>Remarks</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mat_rows_html}
                            <tr style="font-weight: 700; background: rgba(255,255,255,0.03);">
                                <td colspan="4" style="text-align:right;">Total Material Cost:</td>
                                <td colspan="3">{_format_inr(adv_mat_total)}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------------
            # SECTION D: LABOUR REQUIREMENTS
            # ------------------------------------------------------
            st.write("### 👷 Labour Requirements (Section D)")
            lab_rows_list = []
            for _, r in lab_df.iterrows():
                lab_rows_list.append(
                    f"<tr><td>{r['Role']}</td><td>{r['Workers Required']}</td><td>{r['Estimated Working Days']}</td><td>₹{r['Daily Wage']:,.1f}</td><td>₹{r['Estimated Cost']:,.1f}</td></tr>"
                )
            lab_rows_html = "".join(lab_rows_list)

            st.markdown(
                f"""
                <div class="adv-table-wrapper">
                    <table class="adv-custom-table">
                        <thead>
                            <tr>
                                <th>Role / Trade</th>
                                <th>Workers Required</th>
                                <th>Working Days</th>
                                <th>Daily Wage</th>
                                <th>Estimated Cost</th>
                            </tr>
                        </thead>
                        <tbody>
                            {lab_rows_html}
                            <tr style="font-weight: 700; background: rgba(255,255,255,0.03);">
                                <td colspan="4" style="text-align:right;">Total Labour Cost:</td>
                                <td>{_format_inr(adv_lab_total)}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------------
            # SECTION E: MACHINERY REQUIREMENTS
            # ------------------------------------------------------
            st.write("### 🚜 Machinery Sizing & Lease sheet (Section E)")
            mach_rows_list = []
            for _, r in mach_df.iterrows():
                mach_rows_list.append(
                    f"<tr><td>{r['Machine Name']}</td><td>₹{r['Rental Cost']:,.1f}</td><td>{r['Estimated Days']}</td><td>₹{r['Fuel Cost']:,.1f}</td><td>₹{r['Operator Cost']:,.1f}</td><td>₹{r['Maintenance Cost']:,.1f}</td><td>₹{r['Estimated Cost']:,.1f}</td></tr>"
                )
            mach_rows_html = "".join(mach_rows_list)

            st.markdown(
                f"""
                <div class="adv-table-wrapper">
                    <table class="adv-custom-table">
                        <thead>
                            <tr>
                                <th>Machine Name</th>
                                <th>Rental Cost</th>
                                <th>Rental Days</th>
                                <th>Fuel Cost</th>
                                <th>Operator Cost</th>
                                <th>Maintenance</th>
                                <th>Estimated Cost</th>
                            </tr>
                        </thead>
                        <tbody>
                            {mach_rows_html}
                            <tr style="font-weight: 700; background: rgba(255,255,255,0.03);">
                                <td colspan="6" style="text-align:right;">Total Machinery Cost:</td>
                                <td>{_format_inr(adv_mach_total)}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Costs Summary calculations for Section F
            adv_subtotal = adv_mat_total + adv_lab_total + adv_mach_total + adv_trans_cost
            adv_tax = adv_subtotal * TAX_RATE
            adv_contingency = adv_subtotal * CONTINGENCY_RATE
            adv_misc = adv_subtotal * MISC_RATE
            adv_grand_total = adv_subtotal + adv_tax + adv_contingency + adv_misc
            adv_cost_per_sqft = adv_grand_total / building_area if building_area > 0 else 0.0

            adv_summary_map = {
                "Material Cost": adv_mat_total,
                "Labour Cost": adv_lab_total,
                "Machinery Cost": adv_mach_total,
                "Transportation Cost": adv_trans_cost,
                "Miscellaneous Cost": adv_misc,
                "Tax Cost": adv_tax,
                "Contingency Cost": adv_contingency,
                "Grand Total": adv_grand_total,
                "Estimated Cost per Sq Ft": adv_cost_per_sqft
            }

            # ------------------------------------------------------
            # SECTION F: COST BREAKDOWN
            # ------------------------------------------------------
            st.write("### 💰 Financial Breakdown Summary (Section F)")
            adv_dash_cols = st.columns(4)
            with adv_dash_cols[0]:
                render_kpi_card("Material Cost", _format_inr(adv_summary_map["Material Cost"]), "🧱")
                render_kpi_card("GST Tax (18%)", _format_inr(adv_summary_map["Tax Cost"]), "📋")
            with adv_dash_cols[1]:
                render_kpi_card("Labour Cost", _format_inr(adv_summary_map["Labour Cost"]), "👷")
                render_kpi_card("Contingency (10%)", _format_inr(adv_summary_map["Contingency Cost"]), "🛡️")
            with adv_dash_cols[2]:
                render_kpi_card("Machinery Cost", _format_inr(adv_summary_map["Machinery Cost"]), "🚜")
                render_kpi_card("Miscellaneous (5%)", _format_inr(adv_summary_map["Miscellaneous Cost"]), "📦")
            with adv_dash_cols[3]:
                render_kpi_card("Transportation", _format_inr(adv_summary_map["Transportation Cost"]), "🚛")
                adv_rem_budget = st.session_state.adv_budget_limit - adv_grand_total
                budget_badge_color = "#22C55E" if adv_rem_budget >= 0 else "#EF4444"
                render_kpi_card("Remaining Budget", _format_inr(adv_rem_budget), "💵", delta_color=budget_badge_color)

            # Central glow cards
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            bottom_adv_cols = st.columns(2)
            with bottom_adv_cols[0]:
                st.markdown(
                    f"""
                    <div class="cih-kpi-card" style="text-align:center; animation: pulseGlow 2.5s infinite;">
                        <div class="cih-kpi-label">Grand Total Cost</div>
                        <div class="cih-kpi-value" style="font-size:2.1rem; color:#10B981;">{_format_inr(adv_summary_map['Grand Total'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with bottom_adv_cols[1]:
                st.markdown(
                    f"""
                    <div class="cih-kpi-card" style="text-align:center; animation: pulseGlow 2.5s infinite;">
                        <div class="cih-kpi-label">Cost per Square Foot</div>
                        <div class="cih-kpi-value" style="font-size:2rem; color:#3B82F6;">{_format_inr(adv_summary_map['Estimated Cost per Sq Ft'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ------------------------------------------------------
            # SECTION G: VISUAL ANALYTICS
            # ------------------------------------------------------
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("### 📊 Workspace Analytics (Section G)")
            adv_ch_col1, adv_ch_col2 = st.columns(2)
            with adv_ch_col1:
                # 1. Material Distribution
                top_mats_adv = mat_df.nlargest(6, "Estimated Cost")
                oth_cost_adv = mat_df["Estimated Cost"].sum() - top_mats_adv["Estimated Cost"].sum()
                if oth_cost_adv > 0:
                    oth_row_adv = pd.DataFrame([{"Material Name": "Others", "Estimated Cost": oth_cost_adv}])
                    mat_chart_adv = pd.concat([top_mats_adv, oth_row_adv])
                else:
                    mat_chart_adv = top_mats_adv
                
                fig_mat_adv = px.pie(
                    mat_chart_adv, values="Estimated Cost", names="Material Name",
                    color_discrete_sequence=charts.COLORS, hole=0.35
                )
                charts._apply_layout(fig_mat_adv, "Material Cost Distribution", 350)
                st.plotly_chart(fig_mat_adv, use_container_width=True)

                # 3. Machinery Distribution
                fig_mach_adv = px.bar(
                    mach_df, x="Estimated Cost", y="Machine Name", orientation="h",
                    color="Estimated Cost", color_continuous_scale=["#8B5CF6", "#A78BFA", "#C4B5FD"]
                )
                fig_mach_adv.update_coloraxes(showscale=False)
                charts._apply_layout(fig_mach_adv, "Machinery Lease Allocations", 350)
                st.plotly_chart(fig_mach_adv, use_container_width=True)

            with adv_ch_col2:
                # 2. Labour Cost
                fig_lab_adv = px.bar(
                    lab_df, x="Role", y="Estimated Cost", color="Estimated Cost",
                    color_continuous_scale=["#1E40AF", "#3B82F6", "#60A5FA"]
                )
                fig_lab_adv.update_coloraxes(showscale=False)
                charts._apply_layout(fig_lab_adv, "Labour Trade Expenses", 350)
                st.plotly_chart(fig_lab_adv, use_container_width=True)

                # 4. Budget Allocation
                adv_cats_alloc = ["Materials", "Labour", "Machinery", "Transportation", "GST Tax", "Contingency", "Miscellaneous"]
                adv_vals_alloc = [
                    adv_mat_total, adv_lab_total, adv_mach_total, adv_trans_cost, adv_tax, adv_contingency, adv_misc
                ]
                budget_alloc_df = pd.DataFrame({"Category": adv_cats_alloc, "Allocation": adv_vals_alloc})
                fig_budget_adv = px.pie(
                    budget_alloc_df, values="Allocation", names="Category",
                    color_discrete_sequence=charts.COLORS, hole=0.45
                )
                charts._apply_layout(fig_budget_adv, "Overall Project Budget Split", 350)
                st.plotly_chart(fig_budget_adv, use_container_width=True)

            # Export logic setup
            adv_proj_info_dict = {
                "Project Name": st.session_state.adv_project_name,
                "Project ID": st.session_state.adv_project_id,
                "Client Name": st.session_state.adv_client_name,
                "Project Location": st.session_state.adv_project_location,
                "Construction Type": st.session_state.adv_construction_type,
                "Building Category": st.session_state.adv_building_category,
                "Number of Floors": st.session_state.adv_num_floors,
                "Total Plot Area (sq ft)": st.session_state.adv_plot_area,
                "Built-up Area (sq ft)": st.session_state.adv_built_up_area,
                "Duration (Days)": st.session_state.adv_duration_days,
                "Budget Limit": st.session_state.adv_budget_limit
            }

            # Download document option at bottom of workspace
            excel_data_adv = generate_excel_bytes_v2(adv_proj_info_dict, mat_df, lab_df, mach_df, adv_summary_map)
            st.download_button(
                label="📥 Export Excel Estimate (.xlsx)",
                data=excel_data_adv,
                file_name=f"Advanced_Cost_Estimate_{st.session_state.adv_project_id}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="adv_download_excel"
            )

        # Compile Context payload for AI advisor
        advisor_context_str = compile_adv_context_v2(
            {
                "name": st.session_state.adv_project_name,
                "id": st.session_state.adv_project_id,
                "client": st.session_state.adv_client_name,
                "location": st.session_state.adv_project_location,
                "type": st.session_state.adv_construction_type,
                "category": st.session_state.adv_building_category,
                "floors": st.session_state.adv_num_floors,
                "timeline": st.session_state.adv_duration_days,
                "built_up_area": st.session_state.adv_built_up_area
            },
            st.session_state.adv_floors,
            mat_df,
            lab_df,
            mach_df,
            adv_summary_map
        )

        # ------------------------------------------------------
        # SECTION H: AI CONSTRUCTION ADVISOR (Embedded Right Side Panel)
        # ------------------------------------------------------
        with col_ai:
            st.markdown(
                """
                <div class="cih-glass-card" style="margin-bottom: 8px;">
                    <div class="cih-card-title">🤖 AI Construction Advisor (Section H)</div>
                    <p style="margin: 0; font-size: 0.75rem; color: #94A3B8;">Dedicated workspace consultant panel</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Interactive chat history container
            chat_container = st.container(height=420)
            with chat_container:
                for msg in st.session_state.adv_chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
                        
            # Quick inquiries prompt chips
            st.markdown("<p style='font-size:0.7rem; font-weight:600; color:#64748B; margin:8px 0 4px 0;'>QUICK ESTIMATOR INQUIRIES</p>", unsafe_allow_html=True)
            c_chip1, c_chip2 = st.columns(2)
            with c_chip1:
                if st.button("📊 Bill of Quantities", key="chip_boq", use_container_width=True):
                    st.session_state.adv_chat_input = "Generate a basic Bill of Quantities (BOQ)"
                    st.session_state.adv_chat_trigger = True
                if st.button("💸 Reduce Budget", key="chip_reduce", use_container_width=True):
                    st.session_state.adv_chat_input = "Suggest ways to reduce the overall budget"
                    st.session_state.adv_chat_trigger = True
            with c_chip2:
                if st.button("⚖️ Cheaper Materials", key="chip_cheaper", use_container_width=True):
                    st.session_state.adv_chat_input = "Suggest alternative cheaper materials"
                    st.session_state.adv_chat_trigger = True
                if st.button("🚨 Risk Analysis", key="chip_risk", use_container_width=True):
                    st.session_state.adv_chat_input = "Identify potential cost risks"
                    st.session_state.adv_chat_trigger = True
                    
            # Text query input and send button
            user_query = st.text_input("Ask a question about this cost configuration...", key="adv_chat_input_text", value=st.session_state.get("adv_chat_input", ""))
            
            if st.button("💬 Send to AI Advisor", key="adv_send_query_btn", use_container_width=True, type="primary") or st.session_state.get("adv_chat_trigger", False):
                query_to_send = user_query if not st.session_state.get("adv_chat_trigger", False) else st.session_state.adv_chat_input
                st.session_state.adv_chat_input = "" # Reset
                st.session_state.adv_chat_trigger = False # Reset
                
                if query_to_send.strip():
                    # Add user query
                    st.session_state.adv_chat_history.append({"role": "user", "content": query_to_send})
                    
                    with st.spinner("Advisor analyzing project data..."):
                        try:
                            # 1. Format history messages for LLM
                            history_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.adv_chat_history[:-1]]
                            # 2. Query Ollama insights
                            reply_text = ollama_service.insights(query_to_send, history_msgs, advisor_context_str)
                        except Exception as e:
                            # 3. Fallback to local Python simulated advisor
                            reply_text = generate_python_simulated_response(query_to_send, advisor_context_str)
                            
                    st.session_state.adv_chat_history.append({"role": "assistant", "content": reply_text})
                    st.rerun()
                    
            if st.button("🔄 Reset Consultant Conversation", key="adv_reset_chat_btn", use_container_width=True):
                st.session_state.adv_chat_history = [{
                    "role": "assistant",
                    "content": "Welcome to your embedded Construction Estimator AI Advisor. I have parsed your active building layouts, material totals, and machinery rental schedule. Ask me any queries about cost-savings, timelines, or BOQs!"
                }]
                st.rerun()
