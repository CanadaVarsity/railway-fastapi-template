from __future__ import annotations

from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from backend.db import get_database_url

_engine: Engine | None = None
SessionLocal: sessionmaker | None = None


def get_engine() -> Engine | None:
    """
    Central engine for ORM Session usage.
    Keeps your existing behavior: if DATABASE_URL is missing, engine is None.
    """
    global _engine, SessionLocal
    if _engine is not None:
        return _engine

    url = get_database_url()
    if not url:
        _engine = None
        SessionLocal = None
        return None

    _engine = create_engine(url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine


def get_db() -> Generator[Optional[Session], None, None]:
    """
    FastAPI dependency. Yields a Session, or None if DB isn't configured.
    """
    engine = get_engine()
    if engine is None or SessionLocal is None:
        yield None
        return

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
