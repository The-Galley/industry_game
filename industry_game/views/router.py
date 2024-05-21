from fastapi import APIRouter

from industry_game.views.play import router as play_router

router = APIRouter(prefix="/views")
router.include_router(play_router)
