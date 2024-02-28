from typing import Any

import jwt
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_request import Request
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from industry_game.utils.http.auth.base import BaseAuthorizationProvider
from industry_game.utils.users.base import AuthUser
from industry_game.utils.users.models import FullUser

ALGORITHM = "RS256"
AUTH_COOKIE = "industry_game_auth"


class JwtProcessor:
    _private_key: str
    _public_key: str

    def __init__(self, private_key: str, public_key: str) -> None:
        self._private_key = private_key
        self._public_key = public_key

    def encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(
            payload=payload,
            key=self._private_key,
            algorithm=ALGORITHM,
        )

    def decode(self, token: str) -> dict[str, Any] | None:
        try:
            return jwt.decode(
                token,
                key=self._public_key,
                algorithms=[ALGORITHM],
            )
        except jwt.PyJWTError:
            return None


class JwtAuthrorizationProvider(BaseAuthorizationProvider):
    _jwt_processor: JwtProcessor

    def __init__(self, jwt_processor: JwtProcessor) -> None:
        self._jwt_processor = jwt_processor

    def authorize(self, request: Request) -> AuthUser | None:
        token = _get_token_from_cookie(request) or _get_token_from_headers(
            request
        )

        if not token:
            return None

        return self._parse_token(token=token)

    def generate_token(self, user: FullUser) -> str:
        auth_user = AuthUser(id=user.id, username=user.username, type=user.type)
        return self._jwt_processor.encode(payload=auth_user.to_dict())

    def _parse_token(self, token: str) -> AuthUser | None:
        payload = self._jwt_processor.decode(token=token)
        if payload is None:
            return None
        return AuthUser(**payload)


def parse_private_key(private_key: str) -> rsa.RSAPrivateKey:
    return load_pem_private_key(  # type: ignore[return-value]
        private_key.encode(),
        password=None,
    )


def _get_token_from_headers(request: Request) -> str | None:
    raw_value = request.headers.get(AUTHORIZATION)
    if not raw_value:
        return None
    first, _, second = raw_value.partition(" ")
    return second or first


def _get_token_from_cookie(request: Request) -> str | None:
    return request.cookies.get(AUTH_COOKIE)
