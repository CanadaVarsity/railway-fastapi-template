import os
import time
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models import Game

BUILD_STAMP = (
    os.getenv("RAILWAY_DEPLOYMENT_ID")
    or os.getenv("RAILWAY_GIT_COMMIT_SHA")
    or f"manual-{int(time.time())}"
)

router = APIRouter()

@router.get("/games")
def games(db: Optional[Session] = Depends(get_db)):
    if db is None:
        return {
            "build": BUILD_STAMP,
            "marker": "TRUTH_BASELINE",
            "games": [
                {"id": 101, "home": "Montagio Ridge", "away": "Northview", "status": "scheduled"},
                {"id": 102, "home": "Westdale", "away": "Eastport", "status": "final"},
            ],
            "source": "stub",
        }

    rows = db.query(Game).order_by(Game.id).all()
    return {
        "build": BUILD_STAMP,
        "marker": "TRUTH_BASELINE",
        "games": [{"id": r.id, "home": r.home, "away": r.away, "status": r.status} for r in rows],
        "source": "db",
    }
