from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import DATABASE_URL

engine = None
SessionLocal = None

if DATABASE_URL:
    # Railway uses postgres://, SQLAlchemy needs postgresql://
    url = DATABASE_URL.replace("postgres://", "postgresql://", 1) if DATABASE_URL.startswith("postgres://") else DATABASE_URL
    engine = create_engine(url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for FastAPI endpoints"""
    if SessionLocal is None:
        yield None
    else:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
