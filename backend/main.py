import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.router import api_router
from backend.app.db.session import engine
from backend.app.db.base import Base

BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or f"manual-{int(time.time())}"
)

app = FastAPI(
    title="CanadaVarsity API",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (temporary - will use Alembic later)
@app.on_event("startup")
def startup():
    if engine is not None:
        Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(api_router)

# System endpoints
@app.get("/health", tags=["system"])
async def health():
    return {
        "status": "ok",
        "build": BUILD_STAMP,
        "marker": "PHASE2_ORM"
    }

@app.get("/__fingerprint", tags=["system"])
async def fingerprint():
    return {
        "fingerprint": BUILD_STAMP,
        "marker": "PHASE2_ORM",
        "commit": os.getenv("RAILWAY_GIT_COMMIT_SHA"),
        "deployment": os.getenv("RAILWAY_DEPLOYMENT_ID")
    }

@app.get("/", tags=["system"])
async def root():
    return {
        "message": "CanadaVarsity API - Phase 2 (ORM)",
        "build": BUILD_STAMP,
        "docs": "/api/docs",
        "health": "/health",
        "fingerprint": "/__fingerprint",
        "routes": {
            "teams": "/api/v1/teams",
            "games": "/api/v1/games",
        },
    }

@app.get("/__routes", tags=["system"])
def list_routes():
    return sorted([r.path for r in app.routes])
