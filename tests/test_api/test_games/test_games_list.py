from collections.abc import Mapping
from http import HTTPStatus

from aiohttp.test_utils import TestClient
from yarl import URL

from industry_game.utils.users.base import UserType
from tests.utils.datetime import format_tz

API_URL = URL("/api/v1/games/")


async def test_games_list_unauthorized(api_client: TestClient) -> None:
    response = await api_client.get(API_URL)
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_games_list_forbidden(
    api_client: TestClient,
    player_headers: Mapping[str, str],
) -> None:
    response = await api_client.get(API_URL, headers=player_headers)
    assert response.status == HTTPStatus.FORBIDDEN


async def test_games_list_status_ok(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
) -> None:
    response = await api_client.get(API_URL, headers=admin_headers)
    assert response.status == HTTPStatus.OK


async def test_games_list_format_ok(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    create_game,
    create_user,
) -> None:
    admin = await create_user(type=UserType.ADMIN)
    game = await create_game(created_by=admin)
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
        ],
        "meta": {
            "page": 1,
            "page_size": 20,
            "total": 1,
            "pages": 1,
        },
    }
