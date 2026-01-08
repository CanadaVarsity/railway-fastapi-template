import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from backend.db import get_engine as legacy_get_engine
from backend.app.api.v1.router import router as v1_router
from backend.app.core.config import AUTO_CREATE_SCHEMA
from backend.app.db.session import get_engine as orm_get_engine


BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or f"manual-{int(time.time())}"
)

app = FastAPI(
    title="CanadaVarsity API (Truth Baseline)",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_schema_and_seed_legacy_sql() -> None:
    """
    Phase 2 transitional helper.
    - Uses your existing raw SQL approach.
    - Guarded by AUTO_CREATE_SCHEMA so prod can turn this off once Alembic is live.
    """
    engine = legacy_get_engine()
    if engine is None:
        return

    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            school TEXT NOT NULL,
            sport TEXT NOT NULL
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            home TEXT NOT NULL,
            away TEXT NOT NULL,
            status TEXT NOT NULL
        );
        """))

        teams_count = conn.execute(text("SELECT COUNT(*) FROM teams;")).scalar_one()
        if teams_count == 0:
            conn.execute(text("""
                INSERT INTO teams (school, sport) VALUES
                ('Montagio Ridge', 'Football'),
                ('Everest Elementary (demo)', 'Basketball');
            """))

        games_count = conn.execute(text("SELECT COUNT(*) FROM games;")).scalar_one()
        if games_count == 0:
            conn.execute(text("""
                INSERT INTO games (home, away, status) VALUES
                ('Montagio Ridge', 'Northview', 'scheduled'),
                ('Westdale', 'Eastport', 'final');
            """))


@app.on_event("startup")
def startup() -> None:
    # Initialize ORM engine/session (no-op if DATABASE_URL missing)
    orm_get_engine()

    # Only auto-create schema in dev or if explicitly enabled
    if AUTO_CREATE_SCHEMA:
        _ensure_schema_and_seed_legacy_sql()


@app.get("/health", tags=["system"])
async def health():
    db_status = "missing"
    try:
        e = legacy_get_engine()
        if e is not None:
            with e.connect() as conn:
                conn.execute(text("SELECT 1"))
            db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
        "database": db_status,
    }


@app.get("/__fingerprint", tags=["system"])
def fingerprint():
    return {"marker": "TRUTH_BASELINE_RAILWAY", "build": BUILD_STAMP}


@app.get("/__routes", tags=["system"])
def __routes():
    return sorted([r.path for r in app.routes])


@app.get("/", tags=["system"])
async def root():
    return {
        "message": "TRUTH_BASELINE_RUNNING__GIT_TRIGGER_001",
        "build": BUILD_STAMP,
        "service": os.getenv("RAILWAY_SERVICE_NAME", "unknown"),
        "env": os.getenv("RAILWAY_ENVIRONMENT", "unknown"),
        "docs": "/api/docs",
        "openapi": "/api/openapi.json",
        "health": "/health",
        "fingerprint": "/__fingerprint",
        "routes": {
            "status": "/api/v1/status",
            "teams": "/api/v1/teams",
            "games": "/api/v1/games",
        },
    }


# Mount v1 API
app.include_router(v1_router)
