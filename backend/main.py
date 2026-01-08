import os
import time
from fastapi import FastAPI
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
async def v1_teams():
    return {
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
        "teams": [
            {"id": 1, "school": "Montagio Ridge", "sport": "Football"},
            {"id": 2, "school": "Everest Elementary (demo)", "sport": "Basketball"},
        ],
        "source": "stub",
    }

@app.get("/api/v1/games", tags=["v1"])
async def v1_games():
    return {
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
        "games": [
            {"id": 101, "home": "Montagio Ridge", "away": "Northview", "status": "scheduled"},
            {"id": 102, "home": "Westdale", "away": "Eastport", "status": "final"},
        ],
        "source": "stub",
    }

import os, time
BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or os.getenv("RAILWAY_SERVICE_ID")
    or f"manual-{int(time.time())}"
)

@app.get("/__fingerprint", tags=["system"])
def __fingerprint():
    return {"marker": "TRUTH_BASELINE_RAILWAY", "build": BUILD_STAMP}

@app.get("/__routes", tags=["system"])
def __routes():
    return sorted([r.path for r in app.routes])
