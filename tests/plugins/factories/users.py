from collections.abc import Callable
from typing import Any

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import User
from industry_game.utils.security import Passgen


def empty_properties() -> dict[str, Any]:
    return dict()


class UserFactory(SQLAlchemyFactory[User]):
    __set_primary_key__ = False

    properties = empty_properties


@pytest.fixture
def create_user(session: AsyncSession, passgen: Passgen) -> Callable:
    async def factory(**kwargs) -> User:
        password = "secret"
        if "password" in kwargs:
            password = kwargs["password"]
            del kwargs["password"]
        password_hash = passgen.hashpw(password)
        user = UserFactory.build(**kwargs, password_hash=password_hash)
        session.add(user)
        await session.commit()
        await session.flush(user)
        return user

    return factory
