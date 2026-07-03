"""
Task Tracker API - Application Entry Point

This module creates the FastAPI application instance.
CRUD endpoints will be added in a future iteration; this
skeleton currently exposes only a health check endpoint.
"""

from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """
    Health check endpoint.

    Returns a simple JSON payload confirming the service is running,
    along with the current UTC timestamp in ISO 8601 format.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }