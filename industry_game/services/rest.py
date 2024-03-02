from collections.abc import Sequence
from itertools import chain
from typing import Any

import aiohttp_cors
from aiohttp import hdrs
from aiohttp.web import Application
from aiohttp.web_urldispatcher import AbstractRoute
from aiomisc.service.aiohttp import AIOHTTPService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from yarl import URL

from industry_game.handlers.games.create_game import CreateGameHandler
from industry_game.handlers.games.game_details import GameDetailsHandler
from industry_game.handlers.games.game_list import ListGameHandler
from industry_game.handlers.games.game_update import UpdateGameHandler
from industry_game.handlers.games.lobby.add_user_to_lobby import (
    AddUserToGameLobbyHandler,
)
from industry_game.handlers.games.lobby.delete_user_from_lobby import (
    DeleteUserFromLobbyHandler,
)
from industry_game.handlers.games.lobby.list_lobby import ListGameLobbyHandler
from industry_game.handlers.games.lobby.read_lobby import (
    ReadGameUserLobbyHandler,
)
from industry_game.handlers.ping import PingHandler
from industry_game.handlers.players.list_player import ListPlayerHandler
from industry_game.handlers.players.login_player import LoginPlayerHandler
from industry_game.handlers.players.read_by_id_player import (
    ReadByIdPlayerHandler,
)
from industry_game.handlers.players.register_player import RegisterPlayerHandler
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.base import BaseAuthorizationProvider
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.users.processor import PlayerProcessor
from industry_game.utils.users.storage import PlayerStorage

MEGABYTE = 1024**2
ALLOWED_METHODS = (
    hdrs.METH_OPTIONS,
    hdrs.METH_GET,
    hdrs.METH_POST,
    hdrs.METH_DELETE,
)

ApiHandlersType = tuple[tuple[str, str, Any], ...]
NamespacesType = tuple[tuple[str, Any], ...]


class REST(AIOHTTPService):
    __dependencies__ = (
        "game_storage",
        "lobby_storage",
        "player_storage",
        "authorization_provider",
        "session_factory",
        "player_processor",
    )
    __required__ = (
        "access_allow_origins",
        "cors_max_age",
    )

    access_allow_origins: Sequence[URL]
    cors_max_age: int

    game_storage: GameStorage
    lobby_storage: LobbyStorage
    player_storage: PlayerStorage
    authorization_provider: BaseAuthorizationProvider
    player_processor: PlayerProcessor
    session_factory: async_sessionmaker[AsyncSession]

    API_ROUTES: ApiHandlersType = (
        (hdrs.METH_GET, "/api/v1/ping/", PingHandler),
        # user handlers
        (hdrs.METH_GET, "/api/v1/players/", ListPlayerHandler),
        (hdrs.METH_GET, "/api/v1/players/{player_id}/", ReadByIdPlayerHandler),
        (hdrs.METH_POST, "/api/v1/players/login/", LoginPlayerHandler),
        (hdrs.METH_POST, "/api/v1/players/register/", RegisterPlayerHandler),
        # game handlers
        (hdrs.METH_GET, "/api/v1/games/", ListGameHandler),
        (hdrs.METH_POST, "/api/v1/games/", CreateGameHandler),
        (hdrs.METH_GET, "/api/v1/games/{game_id}/", GameDetailsHandler),
        (hdrs.METH_POST, "/api/v1/games/{game_id}/", UpdateGameHandler),
        # lobby handlers
        (hdrs.METH_GET, "/api/v1/games/{game_id}/lobby/", ListGameLobbyHandler),
        (
            hdrs.METH_POST,
            "/api/v1/games/{game_id}/lobby/",
            AddUserToGameLobbyHandler,
        ),
        (
            hdrs.METH_GET,
            "/api/v1/games/{game_id}/lobby/status/",
            ReadGameUserLobbyHandler,
        ),
        (
            hdrs.METH_DELETE,
            "/api/v1/games/{game_id}/lobby/",
            DeleteUserFromLobbyHandler,
        ),
    )
    WS_NAMESPACES: NamespacesType = ()

    async def create_application(self) -> Application:
        app = Application(
            client_max_size=10 * MEGABYTE,
        )
        routes = self._add_routes(app)
        self._add_cors(app, routes)
        self._add_middlewares(app)
        self._add_dependencies(app)
        # self._add_socketio(app)
        return app

    def _add_routes(self, app: Application) -> list[AbstractRoute]:
        return [
            app.router.add_route(
                method=method,
                path=path,
                handler=handler,
            )
            for method, path, handler in self.API_ROUTES
        ]

    def _add_cors(
        self, app: Application, routes: Sequence[AbstractRoute]
    ) -> None:
        resource_options = aiohttp_cors.ResourceOptions(
            allow_headers="*",
            allow_methods=ALLOWED_METHODS,
            allow_credentials=True,
            max_age=self.cors_max_age,
        )
        defaults = {
            str(url): resource_options for url in self.access_allow_origins
        }
        cors = aiohttp_cors.setup(app=app, defaults=defaults)
        for route in routes:
            cors.add(route)

    def _add_middlewares(self, app: Application) -> None:
        pass

    def _add_dependencies(self, app: Application) -> None:
        for name in chain(self.__dependencies__, self.__required__):
            app[name] = getattr(self, name)

    # def _add_socketio(self, app: Application) -> None:
    #     self.sio.attach(app)
    #     deps = {}
    #     for name in chain(self.__dependencies__, self.__required__):
    #         deps[name] = getattr(self, name)

    #     for path, namespace_class in self.WS_NAMESPACES:
    #         namespace = namespace_class(deps=deps, namespace=path)
    #         self.sio.register_namespace(namespace)
