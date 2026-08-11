# Construction Intelligence Hub (CIH)

**Enterprise Construction Management Platform**

A modern, enterprise-grade construction management dashboard built entirely with Python and Streamlit. This frontend prototype provides a centralized platform for managing construction projects, costs, materials, workers, safety, equipment, and progress tracking.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Executive Dashboard** — Real-time KPIs, interactive charts, activity feeds, and system health
- **Project Management** — Full project lifecycle with create, view, and update capabilities
- **Cost Estimation** — Enterprise cost calculator with automatic tax and contingency
- **Material Management** — Inventory tracking with stock progress bars and charts
- **Worker Management** — Workforce directory with attendance and performance analytics
- **Safety Monitoring** — Interactive checklists, safety gauges, and incident tracking
- **Equipment Tracking** — Fleet health cards with maintenance and fuel monitoring
- **Progress Monitoring** — Milestone tracking with Gantt-style visualization
- **Reports** — Multi-format report generation (PDF, Excel, CSV)
- **Settings** — Theme, notifications, language, and user preferences

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Frontend | Streamlit |
| Charts | Plotly |
| Data | Pandas (dummy data) |
| Styling | Custom CSS via `st.markdown()` |

## Project Structure

```
Construction_Intelligence_Hub/
├── app.py                      # Main application entry point
├── modules/
│   ├── dashboard.py            # Executive dashboard
│   ├── project_management.py   # Project CRUD operations
│   ├── cost_estimation.py      # Cost calculator
│   ├── material_management.py  # Inventory management
│   ├── worker_management.py    # Workforce tracking
│   ├── safety_monitoring.py    # Safety compliance
│   ├── equipment_tracking.py   # Fleet monitoring
│   ├── progress_monitoring.py  # Milestone tracking
│   ├── reports.py              # Report generation
│   ├── settings.py             # App configuration
│   └── about.py                # About page
├── utils/
│   ├── charts.py               # Plotly chart builders
│   ├── dummy_data.py           # Sample data generators
│   └── styles.py               # UI styling components
├── assets/
│   └── logo.png                # Application logo
├── requirements.txt
└── README.md
```

## Installation

1. **Clone or navigate to the project directory:**

   ```bash
   cd Construction_Intelligence_Hub
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Generate logo (optional, if not present):**

   ```bash
   python generate_logo.py
   ```

## Running the Application

### Local development

Create or update a local `.env` file with the runtime settings you want to use. The application now reads its configuration from environment variables and `.env` only:

```env
APP_ENV=development
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/cih
```

Then start the app with:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

### Deployment-ready configuration

The same codebase works with deployment environment variables too. For Render, Railway, Docker, or other platforms, provide the same variables in the hosting environment:

```env
APP_ENV=production
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/database
SECRET_KEY=your-secret
JWT_SECRET=your-jwt-secret
```

The startup sequence remains the same in every environment: load configuration, initialize the database if a `DATABASE_URL` is present, initialize backend services, and launch Streamlit.

## UI Design

The interface follows modern SaaS enterprise design principles:

- Dark theme with blue accents (`#0F172A` background, `#3B82F6` accent)
- Glassmorphism cards with frosted glass effects
- Animated KPI cards with hover effects
- Interactive Plotly charts (line, pie, donut, gauge, bar, area)
- Professional sidebar navigation
- Responsive multi-column layouts

## Data

This is a **frontend prototype** with no backend or database. All data is generated using realistic dummy datasets via Pandas DataFrames:

- 25 sample construction projects
- 40 worker records
- 12 material inventory items
- 5 equipment units
- Safety incidents, milestones, and activity feeds

## Credits

- **Project:** Construction Intelligence Hub
- **Version:** 1.0
- **Organization:** Infosys Internship
- **Type:** Frontend Prototype
- **Framework:** Streamlit

## License

This project is developed as an internship prototype for educational purposes.
