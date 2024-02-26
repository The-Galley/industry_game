import logging
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from industry_game.socketio.base import DependenciesNamespace

log = logging.getLogger(__name__)


class Message(BaseModel):
    error: bool
    error_message: str | None = None


class AdminNamespace(DependenciesNamespace):
    async def on_connect(self, sid: str, environ: Mapping[str, Any]) -> None:
        log.info("Connected %s to admin", sid)

    async def on_logout(self, sid: str, environ: Mapping[str, Any]) -> None:
        await self.save_session(sid, {})
        await self.emit(
            event="logout",
            data=Message(error=False).model_dump(mode="json"),
        )

    async def on_disconnect(self, sid: str) -> None:
        pass

    async def on_send(self, sid: str, data: Any) -> None:
        await self.emit(
            event="notify",
            namespace="admin",
            data={"message": "Was sent to admins"},
        )
