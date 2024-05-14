import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from industry_game.db.models import User as UserDb
from industry_game.utils.http.auth.jwt import JwtAuthProvider
from industry_game.utils.security import Passgen
from industry_game.utils.users.base import AuthUser, UserType
from industry_game.utils.users.providers import LoginProvider
from industry_game.utils.users.storage import UserStorage


@pytest.fixture
def user_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> UserStorage:
    return UserStorage(session_factory=session_factory)


@pytest.fixture
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
