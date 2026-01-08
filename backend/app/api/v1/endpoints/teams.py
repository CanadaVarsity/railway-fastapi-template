from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.team import Team
from backend.app.schemas.team import Team as TeamSchema

router = APIRouter()

@router.get("/api/v1/teams", response_model=List[TeamSchema])
def get_teams(db: Session = Depends(get_db)):
    if db is None:
        # Fallback stub data
        return [
            {"id": 1, "school": "Montagio Ridge", "sport": "Football", "league": None, "city": None},
            {"id": 2, "school": "Everest Elementary", "sport": "Basketball", "league": None, "city": None},
        ]
    return db.query(Team).all()
