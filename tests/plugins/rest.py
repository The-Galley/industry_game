from collections.abc import AsyncIterator, Mapping, Sequence

import pytest
from aiohttp import hdrs
from aiohttp.test_utils import TestClient, TestServer
from aiohttp.web_app import Application
from aiomisc import Service
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from yarl import URL

from industry_game.services.rest import REST
from industry_game.utils.buildings.storage import BuildingStorage
from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.auth.base import AuthManager, IAuthProvider
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.users.providers import LoginProvider
from industry_game.utils.users.storage import UserStorage


@pytest.fixture
def rest_url(localhost: str, aiomisc_unused_port_factory) -> URL:
    return URL.build(
        scheme="http",
        host=localhost,
        port=aiomisc_unused_port_factory(),
    )


@pytest.fixture
def rest_service(
    rest_url: URL,
    game_storage: GameStorage,
    lobby_storage: LobbyStorage,
    user_storage: UserStorage,
    building_storage: BuildingStorage,
    login_provider: LoginProvider,
    auth_provider: IAuthProvider,
    session_factory: async_sessionmaker[AsyncSession],
    auth_manager: AuthManager,
) -> REST:
    return REST(
        address=rest_url.host,
        port=rest_url.port,
        game_storage=game_storage,
        lobby_storage=lobby_storage,
        user_storage=user_storage,
        building_storage=building_storage,
        login_provider=login_provider,
        auth_provider=auth_provider,
        session_factory=session_factory,
        auth_manager=auth_manager,
        access_allow_origins=[URL("https://example.com")],
        cors_max_age=3600,
        debug=False,
        project_title="Test",
        project_description="Test description",
        project_version="1.0.0",
    )


@pytest.fixture
def services(rest_service: REST) -> Sequence[Service]:
    return [rest_service]


@pytest.fixture
async def api_client(rest_url: URL) -> AsyncIterator[TestClient]:
    server = TestServer(Application())
    server._root = rest_url

    client = TestClient(server)
    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
def admin_headers(admin_token: str) -> Mapping[str, str]:
    return {hdrs.AUTHORIZATION: admin_token}


@pytest.fixture
def player_headers(player_token: str) -> Mapping[str, str]:
    return {hdrs.AUTHORIZATION: player_token}
