import logging
from collections.abc import Awaitable, Callable, Mapping
from functools import wraps
from typing import Any

from pydantic import ValidationError

from industry_game.socketio.base import DependenciesNamespace, MessageResponse
from industry_game.utils.exceptions import (
    UserNotFoundException,
    UserWithUsernameAlreadExistsException,
)
from industry_game.utils.socketio import validate_data
from industry_game.utils.users.base import AuthUserModel, RegisterPlayerModel

log = logging.getLogger(__name__)

NamespaceFuncType = Callable[
    [DependenciesNamespace, str, Mapping[str, Any]],
    Awaitable[MessageResponse],
]


def message_responser():
    def _wrapper(func: NamespaceFuncType):
        @wraps(func)
        async def _wrapped(
            self: DependenciesNamespace,
            sid: str,
            environ: Mapping[str, Any],
        ) -> None:
            response = await func(self, sid, environ)
            event = func.__name__.split("_")[1]
            await self.emit(
                event=event,
                data=response.model_dump(mode="json"),
                to=sid,
            )

        return _wrapped

    return _wrapper


def validate_model_exception():
    def _wrapper(func: NamespaceFuncType):
        @wraps(func)
        async def _wrapped(
            self: DependenciesNamespace,
            sid: str,
            environ: Mapping[str, Any],
        ):
            try:
                return await func(self, sid, environ)
            except ValidationError as e:
                event = func.__name__.split("_")[1]
                log.warning(
                    "Catch validation error on event %s with data %s",
                    event,
                    environ,
                )
                return MessageResponse(
                    error=True,
                    error_message="Validation error",
                    error_body={"details": e.errors()},
                )

        return _wrapped

    return _wrapper


class PlayerNamespace(DependenciesNamespace):
    async def on_connect(self, sid: str, environ: Mapping[str, Any]) -> None:
        await self.enter_room(sid=sid, room="players")

    @message_responser()
    @validate_model_exception()
    async def on_register(
        self, sid: str, data: Mapping[str, Any]
    ) -> MessageResponse:
        if await self.is_authorized(sid):
            return MessageResponse(body={"message": "User already authorized"})
        user = validate_data(RegisterPlayerModel, data)
        try:
            user = await self.user_processor.register(user)
            log.info("User %s was registered", user.username)
        except UserWithUsernameAlreadExistsException as e:
            return MessageResponse(error=True, error_message=e.message)
        await self.save_session(sid=sid, session={"user": user})
        return MessageResponse(body={"message": "User was registered"})

    @message_responser()
    @validate_model_exception()
    async def on_login(
        self, sid: str, data: Mapping[str, Any]
    ) -> MessageResponse:
        if await self.is_authorized(sid):
            return MessageResponse(body={"message": "User already authorized"})
        user = validate_data(AuthUserModel, data)
        try:
            user = await self.user_processor.login(user)
            log.info("User %s was login", user.username)
        except UserNotFoundException as e:
            return MessageResponse(error=True, error_message=e.message)
        await self.save_session(sid=sid, session={"user": user})
        return MessageResponse(body={"message": "User was logined"})

    async def is_authorized(self, sid: str) -> bool:
        async with self.session(sid) as session:
            return session.get("user") is not None

    async def on_send(self, sid: str, data: Any) -> None:
        await self.emit(
            event="notify",
            room="players",
            data={"message": "Was sent to players"},
        )

    async def on_disconnect(self, sid: str) -> None:
        super().disconnect
