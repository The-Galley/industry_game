from aiohttp.web import View
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_response import Response

from industry_game.utils.http.auth.base import require_authorization
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_path_param
from industry_game.utils.http.response import msgspec_json_response


class ReadByIdGameHandler(View, DependenciesMixin):
    @require_authorization
    async def get(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)
        game = await self.game_storage.read_by_id(game_id=game_id)
        if game is None:
            raise HTTPNotFound
        return msgspec_json_response(obj=game)
