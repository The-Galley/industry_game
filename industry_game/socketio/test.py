from collections.abc import Mapping
from typing import Any

import socketio

from industry_game.utils.timer import Timer


class TestNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid: str, environ: Mapping[str, Any]) -> None:
        pass

    async def on_disconnect(self, sid: str) -> None:
        pass

    async def on_push(self, sid: str, environ: Mapping[str, Any]) -> None:
        await self.emit("my_response", to=sid, data={"accepted": True})
        timer = Timer(self.delayed_send(sid), seconds=27)
        timer.delay()

    async def delayed_send(self, sid: str) -> None:
        await self.emit("delayed", to=sid, data={"this": "is delayed"})

    async def on_message(self, sid: str, environ: Mapping[str, Any]) -> None:
        pass
        await self.emit("message", to=sid, data={"something": "useful"})
