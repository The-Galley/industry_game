from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient
from yarl import URL

from industry_game.utils.http.auth.jwt import AUTH_COOKIE
from industry_game.utils.users.base import UserType

API_URL = URL("/api/v1/players/login/")


async def test_login_empty_json_error(api_client: TestClient):
    response = await api_client.post(API_URL)
    assert response.status == HTTPStatus.BAD_REQUEST


async def test_login_user_not_found_error(api_client: TestClient):
    response = await api_client.post(
        API_URL,
        json={
            "username": "new_user",
            "password": "password",
        },
    )
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_type", (UserType.PLAYER, UserType.ADMIN))
async def test_login_player_successful_status_ok(
    api_client: TestClient, create_user, user_type
):
    player = await create_user(type=user_type)
    response = await api_client.post(
        API_URL,
        json={
            "username": player.username,
            "password": "secret00",
        },
    )
    assert response.status == HTTPStatus.OK


@pytest.mark.parametrize("user_type", (UserType.PLAYER, UserType.ADMIN))
async def test_login_player_successful_format(
    api_client: TestClient,
    token_from_user,
    create_user,
    user_type,
):
    player = await create_user(type=user_type)
    response = await api_client.post(
        API_URL,
        json={
            "username": player.username,
            "password": "secret00",
        },
    )

    result = await response.json()
    assert result == {"token": token_from_user(player)}


@pytest.mark.parametrize("user_type", (UserType.PLAYER, UserType.ADMIN))
async def test_login_player_successful_set_cookie(
    api_client: TestClient,
    token_from_user,
    create_user,
    user_type,
):
    user = await create_user(type=user_type)
    response = await api_client.post(
        API_URL,
        json={
            "username": user.username,
            "password": "secret00",
        },
    )

    assert response.cookies[AUTH_COOKIE].value == token_from_user(user)
