import logging
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.background import BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from industry_game.utils.buildings.storage import BuildingStorage
from industry_game.utils.districts.models import BuildAction
from industry_game.utils.games.controller import GameController
from industry_game.utils.http.auth.jwt import REQUIRE_PLAYER_AUTH
from industry_game.utils.overrides import (
    GetBuildingStorage,
    GetGameController,
    GetTemplates,
)
from industry_game.utils.users.base import AuthUser

log = logging.getLogger(__name__)

router = APIRouter(prefix="/play", tags=["Play"], include_in_schema=False)


@router.get("/{game_id}/")
async def play(
    game_id: int,
    request: Request,
    templates: Jinja2Templates = Depends(GetTemplates),
    game_controller: GameController = Depends(GetGameController),
    auth_user: AuthUser = Depends(REQUIRE_PLAYER_AUTH),
) -> Response:
    game = game_controller.current_games.get(game_id)
    if not game:
        return templates.TemplateResponse(
            name="./errors/404.html.j2",
            context={
                "message": "Game not found",
                "request": request,
            },
            status_code=HTTPStatus.NOT_FOUND,
        )
    log.info("User %s joined game %s", auth_user.id, game_id)
    player = game.players.get(auth_user.id)
    if not player:
        return templates.TemplateResponse(
            name="./errors/403.html.j2",
            context={
                "message": "You are not in this game",
                "request": request,
            },
            status_code=HTTPStatus.FORBIDDEN,
        )

    return templates.TemplateResponse(
        "./play.html.j2",
        {
            "game_id": game_id,
            "district": game.player_districts[auth_user.id],
            "game": game,
            "player": player,
            "apprvs": game.player_districts[auth_user.id].player_approves(
                player
            ),
            "request": request,
        },
        status_code=HTTPStatus.OK,
    )


@router.post("/{game_id}/approve/")
async def approve(
    game_id: int,
    request: Request,
    approve_uuid: Annotated[str, Form()],
    background_tasks: BackgroundTasks,
    templates: Jinja2Templates = Depends(GetTemplates),
    game_controller: GameController = Depends(GetGameController),
    auth_user: AuthUser = Depends(REQUIRE_PLAYER_AUTH),
) -> Response:
    game = game_controller.current_games.get(game_id)
    if not game:
        return templates.TemplateResponse(
            name="./errors/404.html.j2",
            context={
                "message": "Game not found",
                "request": request,
            },
            status_code=HTTPStatus.NOT_FOUND,
        )
    log.info("User %s joined game %s", auth_user.id, game_id)
    player = game.players.get(auth_user.id)
    if not player:
        return templates.TemplateResponse(
            name="./errors/403.html.j2",
            context={
                "message": "You are not in this game",
                "request": request,
            },
            status_code=HTTPStatus.FORBIDDEN,
        )
    district = game.player_districts[player]
    background_tasks.add_task(
        district.approve,
        UUID(approve_uuid),
    )
    return RedirectResponse(url=f"/play/{game_id}/")


@router.post("/{game_id}/build/")
async def build(
    game_id: int,
    request: Request,
    x: Annotated[int, Form()],
    y: Annotated[int, Form()],
    building_id: Annotated[int, Form()],
    templates: Jinja2Templates = Depends(GetTemplates),
    game_controller: GameController = Depends(GetGameController),
    building_storage: BuildingStorage = Depends(GetBuildingStorage),
    auth_user: AuthUser = Depends(REQUIRE_PLAYER_AUTH),
) -> Response:
    game = game_controller.current_games.get(game_id)
    if not game:
        return templates.TemplateResponse(
            name="./errors/404.html.j2",
            context={
                "message": "Game not found",
                "request": request,
            },
            status_code=HTTPStatus.NOT_FOUND,
        )
    log.info("User %s joined game %s", auth_user.id, game_id)
    player = game.players.get(auth_user.id)
    if not player:
        return templates.TemplateResponse(
            name="./errors/403.html.j2",
            context={
                "message": "You are not in this game",
                "request": request,
            },
            status_code=HTTPStatus.FORBIDDEN,
        )

    building = building_storage.get_by_id(building_id=building_id)
    if not building:
        return templates.TemplateResponse(
            name="./errors/404.html.j2",
            context={
                "message": "Building not found",
                "request": request,
            },
            status_code=HTTPStatus.NOT_FOUND,
        )

    district = game.player_districts[player.user_id]
    BuildAction(district=district, building=building, x=x, y=y)
    return RedirectResponse(url=f"/play/{game_id}/")
