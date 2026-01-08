from pydantic import BaseModel
from typing import Optional

class TeamBase(BaseModel):
    school: str
    sport: str
    league: Optional[str] = None
    city: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    
    class Config:
        from_attributes = True
