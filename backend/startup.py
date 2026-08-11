"""Shared hybrid startup sequence for local and cloud execution."""

from __future__ import annotations

from typing import Any, Dict

from backend.app_logging.logger import logger
from backend.config.settings import settings
from backend.database.connection import ping_database
from backend.database.manager import db_manager


def build_startup_context() -> Dict[str, Any]:
    """Build a configuration snapshot for the current runtime environment."""
    database_url = (settings.DATABASE_URL or "").strip()
    backend = "unknown"

    if database_url:
        lowered = database_url.lower()
        if lowered.startswith(("postgresql", "postgres")):
            backend = "postgresql"
        else:
            backend = "postgresql"

    return {
        "app_name": settings.PROJECT_NAME,
        "app_env": settings.APP_ENV,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "database_url_configured": bool(database_url),
        "database_backend": backend,
        "database_ready": False,
        "backend_ready": False,
        "workflow_ready": False,
        "ai_ready": False,
        "startup_status": "not_started",
    }


import streamlit as st


@st.cache_resource(show_spinner=False)
def initialize_hybrid_runtime() -> Dict[str, Any]:
    """Initialize the shared runtime in a deployment-agnostic order (cached per process)."""
    context = build_startup_context()
    logger.info("Starting Construction Intelligence Hub runtime initialization")

    if not context["database_url_configured"]:
        logger.warning("DATABASE_URL is not configured; skipping database initialization")
        context["startup_status"] = "deferred"
        context["backend_ready"] = True
        context["workflow_ready"] = True
        context["ai_ready"] = bool(settings.OLLAMA_HOST)
        return context

    try:
        if ping_database():
            context["database_ready"] = True
            logger.info("Database connectivity verified (schema managed via Alembic)")
        else:
            logger.warning("Database connectivity check failed")
    except Exception as exc:  # pragma: no cover - defensive runtime path
        logger.warning(f"Database connectivity check skipped: {exc}")

    context["backend_ready"] = True
    context["workflow_ready"] = True
    context["ai_ready"] = bool(settings.OLLAMA_HOST)
    context["startup_status"] = "ready" if context["database_ready"] else "degraded"

    try:
        from backend.api.ai_endpoint import start_ai_endpoint_server
        start_ai_endpoint_server()
    except Exception as exc:
        logger.warning(f"AI endpoint startup skipped: {exc}")

    return context
