from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Game
from industry_game.utils.users.base import UserType
from tests.plugins.factories.users import UserFactory


class GameFactory(factory.Factory):
    class Meta:
        model = Game

    id = factory.Sequence(lambda n: n + 1)
    name = "New game"
    description = "New game description"
    finished_at = None
    started_at = None

    created_by = factory.SubFactory(UserFactory, type=UserType.ADMIN)


@pytest.fixture
def create_game(session: AsyncSession) -> Callable:
    async def factory(**kwargs) -> Game:
        game = GameFactory(**kwargs)
        session.add(game)
        await session.commit()
        await session.flush(game)
        return game

    return factory
