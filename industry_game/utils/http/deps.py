from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from industry_game.utils.games.storage import GameStorage
from industry_game.utils.http.base import BaseHttpMixin
from industry_game.utils.lobby.storage import LobbyStorage
from industry_game.utils.users.processor import PlayerProcessor
from industry_game.utils.users.storage import PlayerStorage


class DependenciesMixin(BaseHttpMixin):
    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self.request.app["session_factory"]

    @property
    def game_storage(self) -> GameStorage:
        return self.request.app["game_storage"]

    @property
    def lobby_storage(self) -> LobbyStorage:
        return self.request.app["lobby_storage"]

    @property
    def player_storage(self) -> PlayerStorage:
        return self.request.app["player_storage"]

    @property
    def player_processor(self) -> PlayerProcessor:
        return self.request.app["player_processor"]
