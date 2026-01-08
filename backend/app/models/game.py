from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text

from backend.app.db.base import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    home: Mapped[str] = mapped_column(Text, nullable=False)
    away: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
