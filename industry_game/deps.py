from argparse import Namespace
from collections.abc import AsyncGenerator

import socketio
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from industry_game.socketio.test import TestNamespace
from industry_game.storages.ping import PingStorage
from industry_game.utils.db import create_async_engine, create_async_session_factory


def config_deps(args: Namespace) -> None:
    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            connection_uri=str(args.pg_dsn),
            pool_pre_ping=True,
        )
        yield engine
        await engine.dispose()

    @dependency
    async def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_async_session_factory(engine=engine)

    @dependency
    def ping_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> PingStorage:
        return PingStorage(session_factory=session_factory)

    @dependency
    def sio() -> socketio.AsyncServer:
        server = socketio.AsyncServer(async_mode="aiohttp", logger=True)
        server.register_namespace(TestNamespace("/"))
        return server
