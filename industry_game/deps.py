from argparse import Namespace
from collections.abc import AsyncGenerator

import socketio
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from industry_game.utils.db import (
    create_async_engine,
    create_async_session_factory,
)
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.jwt import (
    JwtAuthrorizationProvider,
    JwtProcessor,
    parse_private_key,
)
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.rsa import stringify_public_key
from industry_game.utils.security import Passgen
from industry_game.utils.users.processor import PlayerProcessor
from industry_game.utils.users.storage import PlayerStorage


def config_deps(args: Namespace) -> None:  # noqa: C901
    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            connection_uri=str(args.pg_dsn),
            pool_pre_ping=True,
        )
        yield engine
        await engine.dispose()

    @dependency
    async def session_factory(
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return create_async_session_factory(engine=engine)

    @dependency
    def game_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> GameStorage:
        return GameStorage(session_factory=session_factory)

    @dependency
    def lobby_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> LobbyStorage:
        return LobbyStorage(session_factory=session_factory)

    @dependency
    def player_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> PlayerStorage:
        return PlayerStorage(session_factory=session_factory)

    @dependency
    def sio() -> socketio.AsyncServer:
        return socketio.AsyncServer(async_mode="aiohttp")

    @dependency
    def jwt_processor() -> JwtProcessor:
        rsa_private_key = parse_private_key(args.private_key)
        public_key = stringify_public_key(rsa_private_key.public_key())
        return JwtProcessor(
            private_key=args.private_key,
            public_key=public_key,
        )

    @dependency
    def authorization_provider(
        jwt_processor: JwtProcessor,
    ) -> JwtAuthrorizationProvider:
        return JwtAuthrorizationProvider(jwt_processor=jwt_processor)

    @dependency
    def passgen() -> Passgen:
        return Passgen(secret=args.secret)

    @dependency
    def player_processor(
        player_storage: PlayerStorage,
        authorization_provider: JwtAuthrorizationProvider,
        passgen: Passgen,
    ) -> PlayerProcessor:
        return PlayerProcessor(
            player_storage=player_storage,
            passgen=passgen,
            authorization_provider=authorization_provider,
        )
