import os
from collections.abc import AsyncIterator
from types import SimpleNamespace

import pytest
from aiomisc_pytest import TCPProxy
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from yarl import URL

from industry_game.db.models import Base
from industry_game.utils.db import (
    create_async_engine,
    make_alembic_config,
)
from tests.utils.db import prepare_new_database, run_async_migrations


@pytest.fixture(scope="session")
def real_db() -> str:
    return "industry_game"


@pytest.fixture(scope="session")
def stairway_db() -> str:
    return "stairway_industry_game"


@pytest.fixture(scope="session")
def real_pg_dsn(localhost: str, real_db: str) -> URL:
    default = f"postgresql+asyncpg://pguser:pguser@{localhost}:5432/{real_db}"
    return URL(os.environ.get("APP_PG_URL", default))


@pytest.fixture(scope="session")
def postgres_pg_dsn(localhost: str) -> URL:
    default = f"postgresql+asyncpg://pguser:pguser@{localhost}:5432/postgres"
    return URL(os.environ.get("APP_BASE_PG_URL", default))


@pytest.fixture()
async def pg_proxy(
    real_pg_dsn: URL,
    localhost: str,
) -> AsyncIterator[TCPProxy]:
    async with TCPProxy(
        target_host=real_pg_dsn.host,
        target_port=real_pg_dsn.port,
        listen_host=localhost,
    ) as proxy:
        yield proxy


@pytest.fixture()
def pg_dsn(real_pg_dsn: URL, pg_proxy: TCPProxy) -> URL:
    return real_pg_dsn.with_host(pg_proxy.proxy_host).with_port(
        pg_proxy.proxy_port
    )


@pytest.fixture(scope="session")
def alembic_config(real_pg_dsn: URL) -> AlembicConfig:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_dsn=str(real_pg_dsn),
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
async def async_engine(
    postgres_pg_dsn: URL,
    pg_dsn: URL,
    real_db: str,
    alembic_config: AlembicConfig,
) -> AsyncIterator[AsyncEngine]:
    await prepare_new_database(
        postgres_pg_dsn=postgres_pg_dsn,
        new_database=real_db,
    )
    await run_async_migrations(alembic_config, Base.metadata, "head")
    engine = create_async_engine(str(pg_dsn))
    yield engine
    await engine.dispose()


@pytest.fixture
def session_factory(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
