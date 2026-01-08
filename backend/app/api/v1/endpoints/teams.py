import os
import time
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models import Team

BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or f"manual-{int(time.time())}"
)

router = APIRouter()

@router.get("/teams")
def teams(db: Optional[Session] = Depends(get_db)):
    if db is None:
        return {
            "build": BUILD_STAMP,
            "marker": "TRUTH_BASELINE",
            "teams": [
                {"id": 1, "school": "Montagio Ridge", "sport": "Football"},
                {"id": 2, "school": "Everest Elementary (demo)", "sport": "Basketball"},
            ],
            "source": "stub",
        }

    rows = db.query(Team).order_by(Team.id).all()
    return {
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
        "teams": [{"id": r.id, "school": r.school, "sport": r.sport} for r in rows],
        "source": "db",
    }
