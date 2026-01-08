from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.game import Game
from backend.app.schemas.game import Game as GameSchema

router = APIRouter()

@router.get("/api/v1/games", response_model=List[GameSchema])
def get_games(db: Session = Depends(get_db)):
    if db is None:
        # Fallback stub data
        return [
            {"id": 101, "home": "Montagio Ridge", "away": "Northview", "status": "scheduled", "sport": None, "date": None},
            {"id": 102, "home": "Westdale", "away": "Eastport", "status": "final", "sport": None, "date": None},
        ]
    return db.query(Game).all()
