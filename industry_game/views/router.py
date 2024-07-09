from fastapi import APIRouter

from industry_game.views.index import router as index_router
from industry_game.views.play import router as play_router

router = APIRouter(prefix="/")
router.include_router(index_router)
router.include_router(play_router)
