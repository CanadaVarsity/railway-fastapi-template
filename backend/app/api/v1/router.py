from fastapi import APIRouter

from backend.app.api.v1.endpoints.status import router as status_router
from backend.app.api.v1.endpoints.teams import router as teams_router
from backend.app.api.v1.endpoints.games import router as games_router

router = APIRouter(prefix="/api/v1")
router.include_router(status_router, tags=["v1"])
router.include_router(teams_router, tags=["v1"])
router.include_router(games_router, tags=["v1"])
