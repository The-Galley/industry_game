from collections.abc import Callable
from datetime import UTC, datetime

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Game, User


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


class GameFactory(SQLAlchemyFactory[Game]):
    __set_primary_key__ = False
    __set_foreign_keys__ = False
    __use_defaults__ = True

    created_at = utc_now
    updated_at = utc_now
    finished_at = None
    started_at = None


@pytest.fixture
def create_game(session: AsyncSession) -> Callable:
    async def factory(created_by: User, **kwargs) -> Game:
        game = GameFactory.build(created_by=created_by, **kwargs)
        session.add(game)
        await session.commit()
        await session.flush(game)
        return game

    return factory
