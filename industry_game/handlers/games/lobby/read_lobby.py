from aiohttp.web import HTTPNotFound, Response, View

from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_player_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_path_param
from industry_game.utils.http.response import msgspec_json_response


class ReadGameUserLobbyHandler(View, DependenciesMixin, AuthMixin):
    @require_player_authorization
    async def get(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)

        game = await self.game_storage.read_by_id(game_id=game_id)
        if game is None:
            raise HTTPNotFound
        return msgspec_json_response(game)
