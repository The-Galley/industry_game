from aiohttp.web import Response, View

from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_player_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_path_param
from industry_game.utils.http.response import msgspec_json_response
from industry_game.utils.lobby.models import LobbyStatus, LobbyStatusType


class ReadGameUserLobbyHandler(View, DependenciesMixin, AuthMixin):
    @require_player_authorization
    async def get(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)

        lobby = await self.lobby_storage.read_by_id(
            game_id=game_id,
            user_id=self.user.id,
        )
        if lobby is None:
            status = LobbyStatusType.NOT_CHECKED_IN
        else:
            status = LobbyStatusType.CHECKED_IN
        return msgspec_json_response(LobbyStatus(status=status))
