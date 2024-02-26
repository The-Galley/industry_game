import abc
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, Concatenate, ParamSpec, TypeVar

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp.web_request import Request

from industry_game.utils.http.base import BaseHttpMixin
from industry_game.utils.typed import not_none
from industry_game.utils.users.base import AuthUser, UserType


class BaseAuthorizationProvider(abc.ABC):
    @abc.abstractmethod
    def authorize(self, request: Request) -> AuthUser | None:
        raise NotImplementedError


class AuthMixin(BaseHttpMixin):
    USER_KEY = "user"

    @property
    def authorization_provider(self) -> BaseAuthorizationProvider | None:
        return self.request.app.get("authorization_provider")

    @property
    def user_or_none(self) -> AuthUser | None:
        if self.USER_KEY not in self.request:
            if not self.authorization_provider:
                user = None
            else:
                user = self.authorization_provider.authorize(self.request)

            self.request[self.USER_KEY] = user

        return self.request[self.USER_KEY]

    @property
    def user(self) -> AuthUser:
        return not_none(self.user_or_none)


TClass = TypeVar("TClass", bound=AuthMixin)
TParams = ParamSpec("TParams")
TResult = TypeVar("TResult")


def _require_user_type_authorization(user_type: UserType | None) -> Callable:
    def require_authorization(
        func: Callable[
            Concatenate[TClass, TParams], Coroutine[Any, Any, TResult]
        ],
    ) -> Callable[Concatenate[TClass, TParams], Coroutine[Any, Any, TResult]]:
        @wraps(func)
        async def wrapper(
            self: TClass, /, *args: TParams.args, **kwargs: TParams.kwargs
        ) -> TResult:
            if self.user_or_none is None:
                raise HTTPUnauthorized

            if user_type is not None:
                if self.user_or_none.type != user_type:
                    raise HTTPForbidden

            return await func(self, *args, **kwargs)

        return wrapper

    return require_authorization


require_player_authorization = _require_user_type_authorization(
    user_type=UserType.PLAYER,
)

require_admin_authorization = _require_user_type_authorization(
    user_type=UserType.ADMIN,
)

require_authorization = _require_user_type_authorization(user_type=None)
