from http import HTTPStatus

import pytest
from aiohttp.test_utils import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from yarl import URL

from industry_game.db.models import User
from industry_game.utils.users.base import UserType

API_URL = URL("/api/v1/users/register/")


async def test_register_successful_status_created(
    api_client: TestClient,
):
    response = await api_client.post(
        API_URL,
        json={
            "username": "username",
            "password": "password",
            "telegram": "telegram",
            "name": "your name",
        },
    )
    assert response.status == HTTPStatus.CREATED


async def test_register_successful_check_db(
    api_client: TestClient,
    session: AsyncSession,
):
    await api_client.post(
        API_URL,
        json={
            "username": "username",
            "password": "password",
            "telegram": "telegram",
            "name": "your name",
        },
    )
    user = (
        await session.scalars(select(User).where(User.username == "username"))
    ).one()

    assert user.username == "username"
    assert user.type == UserType.PLAYER


@pytest.mark.parametrize("user_type", (UserType.ADMIN, UserType.PLAYER))
async def test_register_same_username_error_conflict(
    api_client: TestClient, create_user, user_type
):
    user = await create_user(type=user_type)

    response = await api_client.post(
        API_URL,
        json={
            "username": user.username,
            "password": "password",
            "telegram": "telegram",
            "name": "your name",
        },
    )
    assert response.status == HTTPStatus.BAD_REQUEST
