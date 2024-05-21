from collections.abc import Mapping
from http import HTTPStatus

from aiohttp.test_utils import TestClient
from yarl import URL

API_URL = URL("/api/v1/buildings/")


async def test_buildings_list_unauthorized(api_client: TestClient):
    response = await api_client.get(API_URL)
    assert response.status == HTTPStatus.UNAUTHORIZED


async def test_buildings_list_players_unauthorized(
    api_client: TestClient,
    player_headers: Mapping[str, str],
):
    response = await api_client.get(API_URL, headers=player_headers)
    assert response.status == HTTPStatus.FORBIDDEN


async def test_buildings_list_admins_status_ok(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
):
    response = await api_client.get(API_URL, headers=admin_headers)
    assert response.status == HTTPStatus.OK


async def test_buildings_list_format(
    api_client: TestClient,
    admin_headers: Mapping[str, str],
    create_building,
):
    await create_building()
    response = await api_client.get(API_URL, headers=admin_headers)
    assert await response.json() == {
        "items": [],
        "meta": {"total": 1},
    }
