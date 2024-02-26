import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from industry_game.utils.games.storage import GameStorage


@pytest.fixture
def game_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> GameStorage:
    return GameStorage(session_factory=session_factory)
