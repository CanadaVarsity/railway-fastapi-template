from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text

from backend.app.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    school: Mapped[str] = mapped_column(Text, nullable=False)
    sport: Mapped[str] = mapped_column(Text, nullable=False)
