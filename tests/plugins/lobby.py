import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from industry_game.utils.lobby.storage import LobbyStorage


@pytest.fixture
def lobby_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> LobbyStorage:
    return LobbyStorage(session_factory=session_factory)
