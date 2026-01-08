from fastapi import APIRouter
from backend.app.api.v1.endpoints import teams, games

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(teams.router, tags=["teams"])
api_router.include_router(games.router, tags=["games"])
