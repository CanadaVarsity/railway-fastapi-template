from pydantic import BaseModel
from typing import Optional
from datetime import date

class GameBase(BaseModel):
    home: str
    away: str
    status: str
    sport: Optional[str] = None
    date: Optional[date] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    
    class Config:
        from_attributes = True
