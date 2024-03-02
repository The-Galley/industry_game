from collections.abc import Mapping
from http import HTTPStatus

from aiohttp.test_utils import TestClient
from yarl import URL

from tests.utils.datetime import format_tz

API_URL = URL("/api/v1/games/1/")


async def test_game_details_unauthorized(api_client: TestClient):
    response = await api_client.get(API_URL)
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_game_details_player_status_ok(
    api_client: TestClient,
    player_headers: Mapping[str, str],
    create_game,
):
    await create_game(id=1)
    response = await api_client.get(API_URL, headers=player_headers)
    assert response.status == HTTPStatus.OK


async def test_game_details_player_format(
    api_client: TestClient,
    player_headers: Mapping[str, str],
    create_game,
):
    game = await create_game(id=1)
    response = await api_client.get(API_URL, headers=player_headers)
    result = await response.json()
    assert result == {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "status": game.status.value,
        "created_by_id": game.created_by_id,
        "finished_at": format_tz(game.finished_at),
        "started_at": format_tz(game.started_at),
        "created_at": format_tz(game.created_at),
        "updated_at": format_tz(game.updated_at),
    }


async def test_game_details_admin_status_ok(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    create_game,
):
    await create_game(id=1)
    response = await api_client.get(API_URL, headers=admin_headers)
    assert response.status == HTTPStatus.OK


async def test_game_details_admin_format(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    create_game,
):
    game = await create_game(id=1)
    response = await api_client.get(API_URL, headers=admin_headers)
    result = await response.json()
    assert result == {
        "id": game.id,
        "name": game.name,
        "description": game.description,
        "status": game.status.value,
        "created_by_id": game.created_by_id,
        "finished_at": format_tz(game.finished_at),
        "started_at": format_tz(game.started_at),
        "created_at": format_tz(game.created_at),
        "updated_at": format_tz(game.updated_at),
    }
