from alembic.autogenerate import compare_metadata
from alembic.config import Config as AlembicConfig
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import Connection, MetaData, pool, text
from sqlalchemy.ext.asyncio import AsyncConnection, async_engine_from_config
from yarl import URL

from industry_game.utils.db import create_async_engine


async def run_async_migrations(
    config: AlembicConfig,
    target_metadata: MetaData,
    revision: str,
) -> None:
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs(revision, rev)

    with EnvironmentContext(
        config,
        script=script,
        fn=upgrade,
        as_sql=False,
        starting_rev=None,
        destination_rev=revision,
    ) as context:
        engine = async_engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        async with engine.connect() as connection:
            await connection.run_sync(
                _do_run_migrations,
                target_metadata=target_metadata,
                context=context,
            )


def _do_run_migrations(
    connection: Connection,
    target_metadata: MetaData,
    context: EnvironmentContext,
) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def get_diff_db_metadata(connection: Connection, metadata: MetaData):
    migration_ctx = MigrationContext.configure(connection)
    return compare_metadata(context=migration_ctx, metadata=metadata)


async def prepare_new_database(postgres_pg_dsn: URL, new_database: str) -> None:
    """Using default postgres database for creating new test db"""
    engine = create_async_engine(str(postgres_pg_dsn))
    async with engine.begin() as conn:
        if await _database_exists(conn, new_database):
            await _drop_database(conn, new_database)
        await _create_database(conn, new_database)
    await engine.dispose()


async def _database_exists(conn: AsyncConnection, database: str) -> bool:
    query = f"SELECT 1 from pg_database where datname='{database}'"
    if await conn.scalar(text(query)):
        return True
    return False


async def _create_database(conn: AsyncConnection, database: str) -> None:
    await conn.execute(text("commit"))
    query = "CREATE DATABASE {} ENCODING {} TEMPLATE {}".format(
        database, "utf8", "template1"
    )
    await conn.execute(text(query))


async def _drop_database(conn: AsyncConnection, database: str) -> None:
    await conn.execute(text("commit"))
    await conn.execute(text(f"DROP DATABASE {database}"))
