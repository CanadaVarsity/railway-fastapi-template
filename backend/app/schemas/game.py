from pydantic import BaseModel

class GameOut(BaseModel):
    id: int
    home: str
    away: str
    status: str

    class Config:
        from_attributes = True
