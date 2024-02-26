import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from industry_game.db.models import User as UserDb
from industry_game.utils.http.auth.jwt import JwtAuthrorizationProvider
from industry_game.utils.security import Passgen
from industry_game.utils.users.base import AuthUser, UserType
from industry_game.utils.users.processor import PlayerProcessor
from industry_game.utils.users.storage import PlayerStorage


@pytest.fixture
def player_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> PlayerStorage:
    return PlayerStorage(session_factory=session_factory)

@pytest.fixture
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

@pytest.fixture
def admin() -> AuthUser:
    return AuthUser(
        id=1,
        username="admin",
        type=UserType.ADMIN,
    )


@pytest.fixture
def player() -> AuthUser:
    return AuthUser(
        id=1,
        username="player",
        type=UserType.PLAYER,
    )


@pytest.fixture
def create_admin(admin: AuthUser, session: AsyncSession, passgen: Passgen):
    async def _wrapper(**kwargs) -> UserDb:
        data = admin.to_dict()
        data.update(kwargs)
        if "password_hash" not in data:
            data["password_hash"] = passgen.hashpw("secret")
        user = UserDb(**data)
        session.add(user)
        await session.commit()
        await session.flush(user)
        return user

    return _wrapper
