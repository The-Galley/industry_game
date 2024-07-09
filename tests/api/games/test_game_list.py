from collections.abc import Mapping
from http import HTTPStatus

from aiohttp.test_utils import TestClient
from yarl import URL

from industry_game.db.models import GameStatus
from industry_game.utils.users.base import UserType
from tests.utils.datetime import format_tz

API_URL = URL("/api/v1/games/")


async def test_games_list_unauthorized(api_client: TestClient):
    response = await api_client.get(API_URL)
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_games_list_players_status_ok(
    api_client: TestClient,
    player_headers: Mapping[str, str],
):
    response = await api_client.get(API_URL, headers=player_headers)
    assert response.status == HTTPStatus.OK


async def test_games_list_players_return_only_created_ok(
    api_client: TestClient,
    player_headers: Mapping[str, str],
    create_game,
    create_user,
) -> None:
    admin = await create_user(type=UserType.ADMIN)
    new_game = await create_game(created_by=admin, status=GameStatus.CREATED)
    await create_game(created_by=admin, status=GameStatus.PAUSED)
    response = await api_client.get(API_URL, headers=player_headers)
    result = await response.json()
    assert response.status == HTTPStatus.OK
    assert result == {
        "items": [
            {
                "id": new_game.id,
                "name": new_game.name,
                "description": new_game.description,
                "status": new_game.status.value,
                "created_by_id": admin.id,
                "finished_at": format_tz(new_game.finished_at),
                "started_at": format_tz(new_game.started_at),
                "created_at": format_tz(new_game.created_at),
                "updated_at": format_tz(new_game.updated_at),
            }
        ],
        "meta": {
            "total": 1,
        },
    }


async def test_games_list_admins_status_ok(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
) -> None:
    response = await api_client.get(API_URL, headers=admin_headers)
    assert response.status == HTTPStatus.OK


async def test_games_list_admins_format_ok(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    create_game,
    create_user,
) -> None:
    admin = await create_user(type=UserType.ADMIN)
    new_game = await create_game(created_by=admin)
    paused_game = await create_game(created_by=admin, status=GameStatus.PAUSED)
    response = await api_client.get(API_URL, headers=admin_headers)
    result = await response.json()
    assert result == {
        "items": [
            {
                "id": game.id,
                "name": game.name,
                "description": game.description,
                "status": game.status.value,
                "created_by_id": admin.id,
                "finished_at": format_tz(game.finished_at),
                "started_at": format_tz(game.started_at),
                "created_at": format_tz(game.created_at),
                "updated_at": format_tz(game.updated_at),
            }
            for game in sorted([new_game, paused_game], key=lambda x: x.name)
        ],
        "meta": {
            "total": 2,
        },
    }
