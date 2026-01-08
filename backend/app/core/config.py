import os

DATABASE_URL = os.getenv("DATABASE_URL")
AUTO_CREATE_SCHEMA = os.getenv("AUTO_CREATE_SCHEMA", "false").lower() == "true"
