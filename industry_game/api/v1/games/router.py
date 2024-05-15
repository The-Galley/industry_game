from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field

from industry_game.api.v1.games.lobby import router as lobby_router
from industry_game.db.models import GameStatus
from industry_game.utils.games.controller import GameController
from industry_game.utils.games.models import (
    GameModel,
    GamePaginationModel,
    NewGameModel,
    UpdateGameModel,
)
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.jwt import REQUIRE_ADMIN_AUTH, REQUIRE_AUTH
from industry_game.utils.http.models import StatusResponse
from industry_game.utils.overrides import GetGameController, GetGameStorage
from industry_game.utils.users.base import AuthUser, UserType

router = APIRouter(prefix="/games", tags=["games"])
router.include_router(lobby_router)


@router.get("/")
async def list_games(
    limit: int = Field(default=20, gt=0, le=100),
    offset: int = Field(default=0, gt=-1),
    auth_user: AuthUser = Depends(REQUIRE_AUTH),
    game_storage: GameStorage = Depends(GetGameStorage),
) -> GamePaginationModel:
    if auth_user.type == UserType.ADMIN:
        pagination = await game_storage.pagination(limit=limit, offset=offset)
    else:
        pagination = await game_storage.pagination(
            limit=limit,
            offset=offset,
            status=GameStatus.CREATED,
        )
    return pagination


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.FORBIDDEN: {
            "model": StatusResponse,
            "description": "Forbidden",
        },
    },
)
async def create_game(
    new_game: NewGameModel,
    game_storage: GameStorage = Depends(GetGameStorage),
    auth_user: AuthUser = Depends(REQUIRE_ADMIN_AUTH),
) -> GameModel:
    return await game_storage.create(
        name=new_game.name,
        description=new_game.description,
        created_by_id=auth_user.id,
    )


@router.get("/{game_id}/", dependencies=[Depends(REQUIRE_AUTH)])
async def read_game_by_id(
    game_id: int,
    game_storage: GameStorage = Depends(GetGameStorage),
) -> GameModel:
    game = await game_storage.get_by_id(game_id=game_id)
    if game is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Game not found",
        )
    return GameModel.model_validate(game)


@router.post("/{game_id}/", dependencies=[Depends(REQUIRE_ADMIN_AUTH)])
async def update_game(
    game_id: int,
    update_game: UpdateGameModel,
    game_storage: GameStorage = Depends(GetGameStorage),
) -> GameModel:
    if not update_game.name and not update_game.description:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="No fields to update",
        )
    game = await game_storage.update_text(
        game_id=game_id,
        name=update_game.name,
        description=update_game.description,
    )
    if game is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Game not found",
        )
    return GameModel.model_validate(game)


@router.post("/{game_id}/start", dependencies=[Depends(REQUIRE_ADMIN_AUTH)])
async def start_game(
    game_id: int,
    game_controller: GameController = Depends(GetGameController),
) -> StatusResponse:
    await game_controller.start_game(game_id=game_id)
    return StatusResponse(message=f"Game {game_id} was started")
