from collections.abc import Mapping
from http import HTTPStatus

from aiohttp.test_utils import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from yarl import URL

from industry_game.db.models import Game
from industry_game.utils.users.base import UserType
from tests.utils.datetime import format_tz

API_URL = URL("/api/v1/games/")


async def test_game_create_unauthorized(api_client: TestClient):
    response = await api_client.post(API_URL)
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_game_create_player_forbidden(
    api_client: TestClient,
    player_headers: Mapping[str, str],
):
    response = await api_client.post(API_URL, headers=player_headers)
    assert response.status == HTTPStatus.FORBIDDEN


async def test_game_create_empty_json(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
):
    response = await api_client.post(API_URL, headers=admin_headers)
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_game_create_successful_status_created(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    create_user,
):
    await create_user(type=UserType.ADMIN, id=1)
    response = await api_client.post(
        API_URL,
        headers=admin_headers,
        json={
            "name": "This is new game",
            "description": "This is new game description",
        },
    )
    assert response.status == HTTPStatus.CREATED


async def test_game_create_successful_format(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    session: AsyncSession,
    create_user,
):
    await create_user(type=UserType.ADMIN, id=1)
    response = await api_client.post(
        API_URL,
        headers=admin_headers,
        json={
            "name": "This is new game",
            "description": "This is new game description",
        },
    )
    game = (await session.scalars(select(Game))).one()
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
