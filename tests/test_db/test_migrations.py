import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from yarl import URL

from industry_game.db.models import Base
from tests.utils.db import get_diff_db_metadata, prepare_new_database


@pytest.fixture
async def prepare_stairway_db(
    postgres_pg_dsn: URL,
    stairway_db: str,
):
    await prepare_new_database(
        postgres_pg_dsn=postgres_pg_dsn,
        new_database=stairway_db,
    )


async def test_migrations_up_to_date(async_engine: AsyncEngine) -> None:
    async with async_engine.connect() as connection:
        diff = await connection.run_sync(
            get_diff_db_metadata,
            metadata=(Base.metadata,),
        )
    assert not diff
