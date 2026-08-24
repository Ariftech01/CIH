# Agentic AI for Safety Monitoring with Construction Risk Analytics

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20Supabase%20%7C%20SQLite-007ACC.svg)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🏗️ Project Overview

**Agentic AI for Safety Monitoring with Construction Risk Analytics** is an enterprise construction management and intelligence platform. The platform unites proactive multi-domain risk evaluation, predictive artificial intelligence, comprehensive safety monitoring, interactive 3D Building Information Modeling (BIM) visualization, centralized project management, and consolidated field operations into an intuitive, high-performance web interface.

Designed for construction executives, project directors, site safety officers, structural engineers, and estimators, the application bridges the gap between field execution and strategic risk management.

---

## 🎯 Problem Statement

Modern construction projects generate vast volumes of safety inspections, procurement logs, workforce rosters, equipment telemetry, schedules, and financial records across fragmented sources. Traditional construction management workflows suffer from:

- **Reactive Safety & Risk Response**: Hazards and compliance lapses are frequently discovered after incidents occur rather than preemptively mitigated.
- **Fragmented Operational Data**: Materials, workforce, machinery, and daily progress are tracked in isolated silos, obscuring overall project velocity.
- **Inaccurate Forecasting**: Budget overruns, supply chain delays, and scheduling bottlenecks are identified late due to manual estimations.
- **Unstructured Documentation**: Blueprints, BOQs, and safety audit reports are difficult to synthesize into real-time operational decisions.

**Agentic AI for Safety Monitoring with Construction Risk Analytics** addresses these challenges by delivering a centralized, intelligent control center powered by autonomous AI agents, predictive quantification engines, and live risk scoring.

---

## 🚀 Key Objectives

- **Identify Construction Risks**: Proactively detect structural, environmental, financial, and contractual vulnerabilities.
- **Monitor Site Safety**: Track safety inspections, hazard severity, corrective actions, and regulatory compliance.
- **Deliver Multi-Domain Risk Intelligence**: Aggregate site, safety, compliance, insurance, and operational telemetry into unified risk scores.
- **Provide AI-Assisted Construction Analysis**: Utilize specialized AI models and natural language interfaces for instant domain intelligence.
- **Support Predictive Insights**: Leverage statistical and machine learning models to forecast cost overruns, safety incidents, and schedule delays.
- **Manage Project Lifecycles**: Standardize project registration, budget tracking, BIM metadata, and team allocations.
- **Monitor Construction Operations**: Unify material inventories, worker attendance, machinery utilization, and milestone tracking.
- **Generate Enterprise Reports**: Automatically produce executive summaries, safety audits, and operational reports.

---

## 🧭 Navigation & Module Architecture

The application provides a streamlined navigation hierarchy organized into eight major functional modules:

```
├── 🏠 Dashboard
├── 🛡️ Risk Intelligence
├── 🤖 AI Analysis
├── 🏗️ 3D Building Visualizer
├── 📁 Project Management
├── 🚧 Construction Operations
├── 📄 Reports
└── ⚙ Settings
```

---

### 1. 🏠 Dashboard
The centralized mission control interface providing real-time high-level visibility across all active construction sites:
- **Enterprise KPIs**: Active project counts, total portfolio budget, overall progress percentage, active workforce headcount, and open safety alerts.
- **Project Performance Overview**: Live project status tracking, progress indicators, budget utilization, and assigned site leadership.
- **Operational Metrics**: Quick snapshots of equipment health, material requisitions, and safety inspection statuses.

---

### 2. 🛡️ Risk Intelligence
The flagship multi-domain risk management engine powered by autonomous agents and real-time quantitative scoring:
- **Site Risk Scoring**: Quantitative evaluation of geotechnical, weather, logistics, and site-specific exposure.
- **Safety Assessment**: AI-driven safety hazard classification, OSHA/IS standard compliance checks, and incident tracking.
- **Compliance & Insurance Intelligence**: Regulatory adherence tracking, policy underwriting risk assessments, and contractual risk factors.
- **Historical Risk Analytics**: Trend analysis, risk migration velocity, and snapshot archives.
- **Automated Risk Governance**: Trigger-based risk mitigation recommendations and escalation workflows.

---

### 3. 🤖 AI Analysis
The integrated intelligent assistance and construction prediction engine:
- **Natural-Language Construction Copilot**: Domain-specific conversational assistant tailored for construction engineering, safety protocols, and estimation queries.
- **Document Intelligence (EDMS)**: Context-aware document parsing for BOQs, architectural specifications, and site contracts.
- **Predictive Risk & Cost Forecasting**: Machine learning models predicting cost overruns, safety incident likelihoods, and schedule deviations.
- **Resource & Equipment Analytics**: Predictive optimization of workforce allocation and machinery maintenance intervals.

---

### 4. 🏗️ 3D Building Visualizer
Interactive 3D spatial visualizer for structural models and architectural layouts:
- **Parametric 3D Modeling**: Dynamic 3D rendering of multi-floor structural envelopes, foundations, pillars, and room divisions.
- **BIM Element Inspection**: Interactive inspection of floor-by-floor geometries, room areas, and structural components.
- **Spatial Progress Overlay**: Visual progress mapping across structural levels and zones.

---

### 5. 📁 Project Management
Comprehensive project lifecycle control and integrated cost estimation:
- **All Projects Directory**: Filterable directory of enterprise projects with budget tracking, timelines, and priority levels.
- **Create Master Project Wizard**: Multi-step project creation interface capturing BIM parameters, room configurations, structural details, and leadership assignments.
- **Basic Cost Estimator**: Quick parametric estimation based on built-up area, material grades, and labor rates.
- **Construction Cost Estimator**: Advanced Bill of Quantities (BOQ) cost breakdown across civil works, structural framing, finishing, MEP, and equipment.

---

### 6. 🚧 Construction Operations
The unified operational management module consolidating five critical site domains:
- **Materials Management**: Real-time inventory levels, reorder thresholds, supplier orders, and material delivery logs.
- **Workforce Management**: Daily attendance tracking, trade-wise workforce rosters (masons, electricians, plumbers, laborers), and wage calculations.
- **Safety Monitoring**: Daily inspection records, hazard severity logging (Low, Medium, High, Critical), and corrective action verification.
- **Equipment Tracking**: Machinery status (Operational, Under Maintenance, Idle), health scores, fuel levels, and service schedules.
- **Progress Monitoring**: Milestone completion timelines, planned vs. actual progress tracking, and delay diagnostics.

---

### 7. 📄 Reports
Automated enterprise documentation and audit generation:
- **Comprehensive PDF Reports**: One-click generation of executive summaries, project progress reports, and safety audits.
- **Export Formats**: Multi-format report downloads with formatted KPI cards, risk distribution charts, and tabular appendices.
- **Historical Archives**: Access to previously generated inspection and performance reports.

---

### 8. ⚙ Settings
System configuration and operational preferences:
- **Database & Hybrid Runtime**: Live status of SQLite / PostgreSQL / Supabase connection pooling and table schemas.
- **AI Service Configuration**: Local Ollama host configuration (`http://localhost:11434`), model selection (`llama3.2`), and fallback settings.
- **Theme & Security**: Theme preferences, JWT session policies, and access control settings.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend / UI** | Streamlit (>=1.32.0) | Interactive reactive enterprise web interface |
| **Styling** | Custom CSS + Glassmorphism Tokens | Enterprise UI design with responsive layouts |
| **Language** | Python 3.11 | Core application and backend services runtime |
| **Database & ORM** | SQLAlchemy (>=2.0.0), Alembic (>=1.13.0) | Schema management, migrations, and ORM modeling |
| **Database Engines** | PostgreSQL / Supabase, SQLite | Hybrid enterprise cloud and local database runtime |
| **Data & Analytics** | Pandas, NumPy, Plotly (>=5.18.0) | Data processing, time-series analysis, and charting |
| **AI / LLM Integration** | Ollama, Pydantic (>=2.6.0) | Local AI model inference and structured schema validation |
| **Document Processing** | ReportLab, OpenPyXL, Pillow | PDF report generation, Excel handling, and imaging |
| **Security & Auth** | Passlib, Bcrypt, Python-JOSE | Secure password hashing, RBAC, and session management |
| **Container & Cloud** | Docker, Docker Compose, Render | Multi-stage containerization and cloud deployment |
| **Testing** | Pytest, Python unittest | Automated regression, workflow, and deployment test suites |

---

## 📁 Repository Structure

```
├── app.py                          # Streamlit application entry point & lazy loader
├── assets/
│   └── logo.png                    # Application enterprise branding logo
├── backend/
│   ├── ai_engine/                  # Context engine, prompt builders, intent router
│   ├── analytics/                  # Statistical calculators and metric aggregators
│   ├── api/                        # Internal REST/API gateway & endpoints
│   ├── app_logging/                # Structured enterprise logging subsystem
│   ├── auth/                       # Authentication and role-based permissions
│   ├── automation/                 # Automated task and trigger engines
│   ├── cache/                      # In-memory query caching layers
│   ├── config/                     # Environment configuration and runtime settings
│   ├── database/                   # SQLAlchemy engine, session pools, and health checks
│   ├── document_management/        # EDMS document ingestion and context indexing
│   ├── middleware/                 # Request validation and telemetry middleware
│   ├── models/                     # SQLAlchemy database ORM models
│   ├── observability/              # Telemetry, performance diagnostics, and health
│   ├── prediction_engine/          # Predictive risk and cost forecasting models
│   ├── quantification/             # Risk quantification and scoring algorithms
│   ├── repositories/               # Repository layer for data persistence
│   ├── risk_intelligence/          # Multi-domain risk agents, rules, and scoring
│   ├── schemas/                    # Pydantic validation schemas
│   ├── security/                   # Sanitization and security headers
│   ├── services/                   # Business logic and entity service layer
│   ├── startup.py                  # Hybrid runtime database and service initialization
│   ├── utils/                      # Internal exceptions and shared backend helpers
│   ├── validators/                 # Input data and schema validators
│   ├── workflow/                   # Business workflow state machine
│   ├── init_db.py                  # Database creation and table initialization
│   └── seed.py                     # Initial seed data for development and staging
├── migrations/
│   ├── versions/                   # Alembic schema migration scripts
│   ├── env.py                      # Alembic migration environment
│   └── script.py.mako              # Migration template
├── modules/
│   ├── __init__.py
│   ├── dashboard.py                # Dashboard module
│   ├── construction_risk.py        # Risk Intelligence module
│   ├── ai_analysis.py              # AI Analysis module
│   ├── building_visualizer.py      # 3D Building Visualizer module
│   ├── project_management.py       # Project Management & Cost Estimator module
│   ├── construction_operations.py  # Consolidated Operations module
│   ├── cost_estimation.py          # Detailed Cost Estimation component
│   ├── reports.py                  # Reports module
│   └── settings.py                 # Settings module
├── services/
│   └── ollamaService.py            # Local Ollama AI service integration
├── utils/
│   ├── auth.py                     # Streamlit authentication gateway and UI login
│   ├── charts.py                   # Reusable Plotly chart builders
│   ├── dashboard_components.py     # KPI cards and overview components
│   ├── dummy_data.py               # Fallback mock datasets
│   ├── profiler.py                 # Execution latency profiling utilities
│   └── styles.py                   # Master CSS design system and theme injection
├── tests/
│   ├── test_ai_pipeline_regressions.py  # AI guardrails & context retrieval tests
│   ├── test_auth.py                     # Authentication & password hashing tests
│   ├── test_database.py                 # Database connectivity & session tests
│   ├── test_hybrid_configuration.py     # Runtime configuration & API tests
│   ├── test_models.py                   # ORM model integrity tests
│   ├── test_production_deployment.py    # Production deployment readiness tests
│   ├── test_project_workflow_sync.py    # Workflow synchronization tests
│   ├── test_repositories.py             # Repository layer CRUD tests
│   ├── test_services.py                 # Service layer business logic tests
│   ├── test_workflow.py                 # Workflow automation tests
│   ├── benchmark_performance.py         # Performance benchmark harness
│   ├── run_production_tests.py          # Production test runner
│   ├── run_tests.py                     # Master unit test suite runner
│   └── run_workflow_tests.py            # End-to-end workflow test runner
├── .github/
│   └── workflows/
│       └── ci_cd.yml               # GitHub Actions CI/CD automated test pipeline
├── .dockerignore                   # Docker build ignore patterns
├── .env.example                    # Clean environment configuration template
├── .gitignore                      # Git ignore configuration
├── alembic.ini                     # Alembic configuration
├── docker-compose.yml              # Multi-container orchestration
├── Dockerfile                      # Production multi-stage Docker container build
├── LICENSE                         # MIT License
├── render.yaml                     # Cloud deployment configuration
└── requirements.txt                # Python package dependencies
```

---

## ⚡ Installation & Local Setup

### Prerequisites
- **Python 3.11+** installed on your system.
- **Git** installed.
- *(Optional)* **Ollama** installed with `llama3.2` model downloaded (`ollama pull llama3.2`) for local AI copilot execution.

---

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Construction_Intelligence_Hub
   ```

2. **Create and Activate a Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy the example environment file and configure your database and API settings:
   - **Windows**:
     ```powershell
     Copy-Item .env.example .env
     ```
   - **Linux / macOS**:
     ```bash
     cp .env.example .env
     ```

5. **Initialize the Database**:
   Create database tables and seed baseline sample data:
   ```bash
   python backend/init_db.py
   python backend/seed.py
   ```

6. **Launch the Application**:
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## 🔐 Environment Variables Reference

Configure environment parameters in your `.env` file:

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `APP_ENV` | Application environment mode (`development`, `testing`, `production`) | `development` |
| `DEBUG` | Enable verbose debugging and stack traces | `True` |
| `DATABASE_URL` | SQLAlchemy database connection string (SQLite, PostgreSQL, Supabase) | `sqlite:///./construction_intelligence_hub.db` |
| `SUPABASE_URL` | *(Optional)* Supabase project URL | `https://your-project.supabase.co` |
| `SUPABASE_ANON_KEY` | *(Optional)* Supabase anonymous public key | `your-anon-key` |
| `SUPABASE_SERVICE_ROLE_KEY` | *(Optional)* Supabase service role key | `your-service-key` |
| `SSL_MODE` | PostgreSQL SSL connection mode (`prefer`, `require`) | `prefer` |
| `SECRET_KEY` | Application encryption and session security key | `your-secure-secret-key-32-chars-long` |
| `JWT_SECRET` | JSON Web Token signing secret | `your-secure-jwt-secret-32-chars-long` |
| `OLLAMA_HOST` | Host URL for local Ollama AI model server | `http://localhost:11434` |
| `MODEL_NAME` | Name of the local LLM model for AI Analysis | `llama3.2` |

---

## 🧪 Testing

The repository contains automated unit, regression, workflow, and deployment validation suites:

- **Run Full Unit & Regression Test Suite**:
  ```bash
  python tests/run_tests.py
  ```

- **Run End-to-End Workflow Tests**:
  ```bash
  python tests/run_workflow_tests.py
  ```

- **Run Production Deployment Verification Tests**:
  ```bash
  python tests/run_production_tests.py
  ```

- **Run via Pytest**:
  ```bash
  pytest tests/
  ```

---

## 🚢 Deployment

### Docker Container Deployment
Build and run the production multi-stage Docker container:

```bash
docker build -t construction-intelligence-hub:latest .
docker run -d -p 8501:8501 --env-file .env construction-intelligence-hub:latest
```

Or using Docker Compose:
```bash
docker-compose up -d --build
```

### Cloud Deployment (Render)
The project includes a production [`render.yaml`](render.yaml) blueprint:
1. Connect your GitHub repository to Render.
2. Deploy as a Web Service using the preconfigured blueprint.
3. Configure your production environment variables (`DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET`) in the Render dashboard.

---

## 🔒 Security & Privacy

- **Never Commit Secrets**: Ensure `.env` is listed in `.gitignore` and never committed to version control.
- **Safe Fallbacks**: The system operates smoothly in disconnected mode with local SQLite and intelligent fallback engines when external LLMs or remote databases are unreachable.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

