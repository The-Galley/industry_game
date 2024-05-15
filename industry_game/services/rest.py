from collections.abc import Callable
from http import HTTPMethod

from aiomisc.service.uvicorn import UvicornApplication, UvicornService
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.middleware.cors import CORSMiddleware

from industry_game.api.router import router as api_router
from industry_game.utils.buildings.storage import BuildingStorage
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.base import AuthManager
from industry_game.utils.http.auth.jwt import (
    MAYBE_AUTH,
    REQUIRE_ADMIN_AUTH,
    REQUIRE_AUTH,
    REQUIRE_PLAYER_AUTH,
)
from industry_game.utils.http.exceptions.handlers import http_exception_handler
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.overrides import (
    GetBuildingStorage,
    GetGameStorage,
    GetLobbyStorage,
    GetLoginProvider,
    GetSessionFactory,
    GetTemplates,
    GetUserStorage,
)
from industry_game.utils.users.providers import LoginProvider
from industry_game.utils.users.storage import UserStorage

ExceptionHandlersType = tuple[tuple[type[Exception], Callable], ...]


class REST(UvicornService):
    __required__ = (
        "debug",
        "project_title",
        "project_description",
        "project_version",
    )
    __dependencies__ = (
        "session_factory",
        "auth_manager",
        "login_provider",
        "user_storage",
        "game_storage",
        "lobby_storage",
        "building_storage",
    )
    EXCEPTION_HANDLERS: ExceptionHandlersType = (
        (HTTPException, http_exception_handler),
    )

    debug: bool
    project_title: str
    project_description: str
    project_version: str

    session_factory: async_sessionmaker[AsyncSession]
    auth_manager: AuthManager
    login_provider: LoginProvider
    user_storage: UserStorage
    game_storage: GameStorage
    lobby_storage: LobbyStorage
    building_storage: BuildingStorage
    templates: Jinja2Templates

    async def create_application(self) -> UvicornApplication:
        app = FastAPI(
            debug=self.debug,
            title=self.project_title,
            description=self.project_description,
            version=self.project_version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
        )
        self._add_middlewares(app)
        self._add_routes(app)
        self._add_exceptions(app)
        self._add_dependency_overrides(app)
        self._add_static(app)
        return app

    def _add_middlewares(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=[
                HTTPMethod.OPTIONS,
                HTTPMethod.GET,
                HTTPMethod.HEAD,
                HTTPMethod.POST,
                HTTPMethod.DELETE,
            ],
            allow_headers=["*"],
        )

    def _add_routes(self, app: FastAPI) -> None:
        app.include_router(api_router)

    def _add_exceptions(self, app: FastAPI) -> None:
        for exception, handler in self.EXCEPTION_HANDLERS:
            app.add_exception_handler(exception, handler)

    def _add_dependency_overrides(self, app: FastAPI) -> None:
        app.dependency_overrides.update(
            {
                MAYBE_AUTH: self.auth_manager.maybe_auth,
                REQUIRE_AUTH: self.auth_manager.require_auth,
                REQUIRE_ADMIN_AUTH: self.auth_manager.require_admin_auth,
                REQUIRE_PLAYER_AUTH: self.auth_manager.require_player_auth,
                GetSessionFactory: lambda: self.session_factory,
                GetUserStorage: lambda: self.user_storage,
                GetLoginProvider: lambda: self.login_provider,
                GetGameStorage: lambda: self.game_storage,
                GetLobbyStorage: lambda: self.lobby_storage,
                GetBuildingStorage: lambda: self.building_storage,
                GetTemplates: lambda: self.templates,
            }
        )

    def _add_static(self, app: FastAPI) -> None:
        app.mount("/static", StaticFiles(directory="static"), name="static")
