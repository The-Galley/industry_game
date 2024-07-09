from fastapi import APIRouter

from industry_game.api.v1.buildings import router as building_router
from industry_game.api.v1.games.router import router as games_router
from industry_game.api.v1.monitoring import router as monitoring_router
from industry_game.api.v1.users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(monitoring_router)
router.include_router(users_router)
router.include_router(games_router)
router.include_router(building_router)
