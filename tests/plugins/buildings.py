import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from industry_game.utils.buildings.storage import BuildingStorage


@pytest.fixture
def building_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> BuildingStorage:
    return BuildingStorage(session_factory=session_factory)
