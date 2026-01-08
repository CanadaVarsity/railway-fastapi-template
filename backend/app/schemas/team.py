from pydantic import BaseModel

class TeamOut(BaseModel):
    id: int
    school: str
    sport: str

    class Config:
        from_attributes = True
