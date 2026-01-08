import os
import time
from fastapi import FastAPI
from sqlalchemy import text
from backend.db import get_engine
from fastapi.middleware.cors import CORSMiddleware

BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or f"manual-{int(time.time())}"
)

app = FastAPI(
    title="CanadaVarsity API (Truth Baseline)",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


def _ensure_schema_and_seed():
    engine = get_engine()
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
def startup():
    _ensure_schema_and_seed()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "build": BUILD_STAMP, "marker": "TRUTH_BASELINE"}

@app.get("/__fingerprint", tags=["system"])
async def fingerprint():
    return {"fingerprint": BUILD_STAMP, "marker": "TRUTH_BASELINE"}

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

@app.get("/api/v1/status", tags=["v1"])
async def v1_status():
    return {
        "status": "operational_DEPLOY_PROOF_1767757600",
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
    }


@app.get("/api/v1/teams", tags=["v1"])
def teams():
    engine = get_engine()
    if engine is None:
        return {
            "build": BUILD_STAMP,
            "marker": "TRUTH_BASELINE",
            "teams": [
                {"id": 1, "school": "Montagio Ridge", "sport": "Football"},
                {"id": 2, "school": "Everest Elementary (demo)", "sport": "Basketball"},
            ],
            "source": "stub",
        }

    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id, school, sport FROM teams ORDER BY id;")).mappings().all()
        return {
            "build": BUILD_STAMP,
            "marker": "TRUTH_BASELINE",
            "teams": [dict(r) for r in rows],
            "source": "db",
        }



@app.get("/api/v1/games", tags=["v1"])
def games():
    engine = get_engine()
    if engine is None:
        return {
            "build": BUILD_STAMP,
            "marker": "TRUTH_BASELINE",
            "games": [
                {"id": 101, "home": "Montagio Ridge", "away": "Northview", "status": "scheduled"},
                {"id": 102, "home": "Westdale", "away": "Eastport", "status": "final"},
            ],
            "source": "stub",
        }

    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id, home, away, status FROM games ORDER BY id;")).mappings().all()
        return {
            "build": BUILD_STAMP,
            "marker": "TRUTH_BASELINE",
            "games": [dict(r) for r in rows],
            "source": "db",
        }


@app.get("/__fingerprint", tags=["system"])
def __fingerprint():
    return {"marker": "TRUTH_BASELINE_RAILWAY", "build": BUILD_STAMP}

@app.get("/__routes", tags=["system"])
def __routes():
    return sorted([r.path for r in app.routes])
