from fastapi import APIRouter

router = APIRouter(prefix="", tags=["lobby"])


@router.get("/{game_id}/lobby/")
async def list_game_lobby() -> None:
    pass


@router.post("/{game_id}/lobby/")
async def add_user_to_game_lobby() -> None:
    pass


@router.get("/{game_id}/lobby/status/")
async def read_game_lobby_status() -> None:
    pass


@router.delete("/{game_id}/lobby/")
async def delete_user_from_game_lobby() -> None:
    pass
