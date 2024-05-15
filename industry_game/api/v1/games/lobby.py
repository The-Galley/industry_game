from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import Field

from industry_game.db.models import GameStatus
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.jwt import (
    REQUIRE_ADMIN_AUTH,
    REQUIRE_PLAYER_AUTH,
)
from industry_game.utils.lobby.models import (
    LobbyPaginationModel,
    LobbyStatus,
    LobbyStatusType,
)
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.overrides import GetGameStorage, GetLobbyStorage
from industry_game.utils.users.base import AuthUser

router = APIRouter(prefix="", tags=["lobby"])


@router.get("/{game_id}/lobby/", dependencies=[Depends(REQUIRE_ADMIN_AUTH)])
async def list_game_lobby(
    game_id: int,
    limit: int = Field(default=20, gt=0, le=100),
    offset: int = Field(default=0, gt=-1),
    game_storage: GameStorage = Depends(GetGameStorage),
    lobby_storage: LobbyStorage = Depends(GetLobbyStorage),
) -> LobbyPaginationModel:
    game = await game_storage.get_by_id(game_id=game_id)
    if game is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Game not found",
        )
    return await lobby_storage.pagination(
        game_id=game_id,
        limit=limit,
        offset=offset,
    )


@router.post("/{game_id}/lobby/")
async def add_user_to_game_lobby(
    game_id: int,
    game_storage: GameStorage = Depends(GetGameStorage),
    lobby_storage: LobbyStorage = Depends(GetLobbyStorage),
    auth_user: AuthUser = Depends(REQUIRE_PLAYER_AUTH),
) -> Response:
    game = await game_storage.get_by_id(game_id=game_id)
    if game is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Game not found",
        )
    if game.status != GameStatus.CREATED:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Game already started",
        )
    lobby = await lobby_storage.read_by_id(
        game_id=game_id,
        user_id=auth_user.id,
    )
    if lobby is not None:
        return Response(status_code=HTTPStatus.OK)
    await lobby_storage.add_user(game_id=game_id, user_id=auth_user.id)
    return Response(status_code=HTTPStatus.CREATED)


@router.get("/{game_id}/lobby/status/")
async def read_game_lobby_status(
    game_id: int,
    lobby_storage: LobbyStorage = Depends(GetLobbyStorage),
    auth_user: AuthUser = Depends(REQUIRE_PLAYER_AUTH),
) -> LobbyStatus:
    lobby = await lobby_storage.read_by_id(
        game_id=game_id,
        user_id=auth_user.id,
    )
    if lobby is None:
        status = LobbyStatusType.NOT_CHECKED_IN
    else:
        status = LobbyStatusType.CHECKED_IN
    return LobbyStatus(status=status)


@router.delete("/{game_id}/lobby/")
async def delete_user_from_game_lobby(
    game_id: int,
    game_storage: GameStorage = Depends(GetGameStorage),
    lobby_storage: LobbyStorage = Depends(GetLobbyStorage),
    auth_user: AuthUser = Depends(REQUIRE_PLAYER_AUTH),
) -> Response:
    game = await game_storage.get_by_id(game_id=game_id)
    if game is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Game not found",
        )
    if game.status != GameStatus.CREATED:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Game already started",
        )
    await lobby_storage.delete(game_id=game_id, user_id=auth_user.id)
    return Response(status_code=HTTPStatus.NO_CONTENT)
