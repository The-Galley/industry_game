from aiohttp.web import Response, View

from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_admin_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.models import StatusResponse
from industry_game.utils.http.params import parse_path_param
from industry_game.utils.http.response import msgspec_json_response


class StartGameHandler(View, DependenciesMixin, AuthMixin):
    @require_admin_authorization
    async def post(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)
        await self.game_store.start_game(game_id=game_id)
        return msgspec_json_response(
            StatusResponse(message=f"Game {game_id} was started")
        )
