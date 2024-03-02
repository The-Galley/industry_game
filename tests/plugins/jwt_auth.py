from collections.abc import Callable

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from industry_game.db.models import User
from industry_game.utils.http.auth.jwt import (
    JwtAuthrorizationProvider,
    JwtProcessor,
)
from industry_game.utils.rsa import (
    get_private_key,
    stringify_private_key,
    stringify_public_key,
)
from industry_game.utils.users.base import AuthUser


@pytest.fixture(scope="session")
def private_key() -> rsa.RSAPrivateKey:
    return get_private_key()


@pytest.fixture(scope="session")
def private_key_str(private_key: rsa.RSAPrivateKey) -> str:
    return stringify_private_key(private_key)


@pytest.fixture(scope="session")
def public_key_str(private_key: rsa.RSAPrivateKey) -> str:
    public_key = private_key.public_key()
    return stringify_public_key(public_key)


@pytest.fixture
def jwt_processor(private_key_str: str, public_key_str: str) -> JwtProcessor:
    return JwtProcessor(
        private_key=private_key_str,
        public_key=public_key_str,
    )


@pytest.fixture
def authorization_provider(
    jwt_processor: JwtProcessor,
) -> JwtAuthrorizationProvider:
    return JwtAuthrorizationProvider(jwt_processor=jwt_processor)


@pytest.fixture
def admin_token(admin: AuthUser, jwt_processor: JwtProcessor) -> str:
    return jwt_processor.encode(admin.to_dict())


@pytest.fixture
def player_token(player: AuthUser, jwt_processor: JwtProcessor) -> str:
    return jwt_processor.encode(player.to_dict())


@pytest.fixture
def token_from_user(jwt_processor: JwtProcessor) -> Callable:
    def _factory(user: User) -> str:
        return jwt_processor.encode(
            {
                "id": user.id,
                "username": user.username,
                "type": user.type,
            }
        )

    return _factory
