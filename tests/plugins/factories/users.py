from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import User
from industry_game.utils.security import Passgen
from industry_game.utils.users.base import UserType


class UserPropertiesFactory(factory.Factory):
    class Meta:
        model = dict

    name = "First Last Name"
    telegram = "@tg_username"


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    username = "username"
    type = UserType.PLAYER
    password_hash = ""
    properties = factory.SubFactory(UserPropertiesFactory)


@pytest.fixture
def create_user(session: AsyncSession, passgen: Passgen) -> Callable:
    async def factory(**kwargs) -> User:
        password = kwargs.get("password", "secret00")
        if "password" in kwargs:
            del kwargs["password"]
        kwargs["password_hash"] = passgen.hashpw(password)
        user = UserFactory(**kwargs)
        session.add(user)
        await session.commit()
        await session.flush(user)
        return user

    return factory
