import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

def get_engine() -> Engine | None:
    url = get_database_url()
    if not url:
        return None
    return create_engine(url, pool_pre_ping=True)
