from argparse import Namespace
from collections import deque
from collections.abc import AsyncGenerator
from pathlib import Path

from aiomisc_dependency import dependency
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from industry_game.init_data import create_game
from industry_game.utils.buildings.storage import BuildingStorage
from industry_game.utils.db import (
    create_async_engine,
    create_async_session_factory,
)
from industry_game.utils.events.base import AbstractEvent
from industry_game.utils.games.controller import GameController
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.base import AuthManager, IAuthProvider
from industry_game.utils.http.auth.jwt import (
    JwtAuthProvider,
    JwtProcessor,
    parse_private_key,
)
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.rsa import stringify_public_key
from industry_game.utils.security import Passgen
from industry_game.utils.users.providers import LoginProvider
from industry_game.utils.users.storage import UserStorage

PROJECT_ROOT = Path(__file__).parent.resolve()


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
    def user_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> UserStorage:
        return UserStorage(session_factory=session_factory)

    @dependency
    def building_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> BuildingStorage:
        return BuildingStorage(session_factory=session_factory)

    @dependency
    def jwt_processor() -> JwtProcessor:
        rsa_private_key = parse_private_key(args.private_key)
        public_key = stringify_public_key(rsa_private_key.public_key())
        return JwtProcessor(
            private_key=args.private_key,
            public_key=public_key,
        )

    @dependency
    def auth_provider(
        jwt_processor: JwtProcessor,
    ) -> JwtAuthProvider:
        return JwtAuthProvider(jwt_processor=jwt_processor)

    @dependency
    def passgen() -> Passgen:
        return Passgen(secret=args.secret)

    @dependency
    def auth_manager(auth_provider: IAuthProvider) -> AuthManager:
        return AuthManager(auth_provider=auth_provider)

    @dependency
    def login_provider(
        user_storage: UserStorage,
        auth_provider: JwtAuthProvider,
        passgen: Passgen,
    ) -> LoginProvider:
        return LoginProvider(
            user_storage=user_storage,
            passgen=passgen,
            auth_provider=auth_provider,
        )

    @dependency
    def templates() -> Jinja2Templates:
        return Jinja2Templates(directory=PROJECT_ROOT / "templates")

    @dependency
    def event_queue() -> deque[AbstractEvent]:
        return deque()

    @dependency
    def game_controller(
        game_storage: GameStorage,
        event_queue: deque[AbstractEvent],
    ) -> GameController:
        return GameController(
            game_storage=game_storage,
            current_games={
                1: create_game(),
            },
            event_queue=event_queue,
        )
