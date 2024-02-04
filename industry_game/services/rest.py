from itertools import chain
from typing import Any

import socketio
from aiohttp import hdrs
from aiohttp.web import Application
from aiomisc.service.aiohttp import AIOHTTPService

from industry_game.handlers.ping import PingHandler
from industry_game.storages.ping import PingStorage

MEGABYTE = 1024**2

HandlersType = tuple[tuple[str, str, Any], ...]


class REST(AIOHTTPService):
    __dependencies__ = (
        "ping_storage",
        "sio",
    )
    sio: socketio.AsyncServer
    ping_storage: PingStorage

    ROUTES: HandlersType = ((hdrs.METH_GET, "/api/v1/ping/", PingHandler),)

    async def create_application(self) -> Application:
        app = Application(
            client_max_size=10 * MEGABYTE,
        )
        self._add_routes(app)
        self._add_middlewares(app)
        self._add_dependencies(app)
        self._add_socketio(app)
        return app

    def _add_routes(self, app: Application) -> None:
        for method, path, handler in self.ROUTES:
            app.router.add_route(method=method, path=path, handler=handler)

    def _add_middlewares(self, app: Application) -> None:
        pass

    def _add_dependencies(self, app: Application) -> None:
        for name in chain(self.__dependencies__, self.__required__):
            app[name] = getattr(self, name)

    def _add_socketio(self, app: Application) -> None:
        self.sio.attach(app)
