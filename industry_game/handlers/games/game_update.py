from aiohttp.web import View
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import Response

from industry_game.utils.games.models import UpdateGameModel
from industry_game.utils.http.auth.base import AuthMixin
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_json_model, parse_path_param
from industry_game.utils.http.response import msgspec_json_response


class UpdateGameHandler(View, DependenciesMixin, AuthMixin):
    async def post(self) -> Response:
        body = await self.request.read()
        update_game_data = parse_json_model(model=UpdateGameModel, data=body)
        if not update_game_data.name and not update_game_data.description:
            raise HTTPBadRequest
        game_id = parse_path_param(self.request, "game_id", int)
        game = await self.game_storage.update(
            game_id=game_id,
            name=update_game_data.name,
            description=update_game_data.description,
        )
        return msgspec_json_response(game)
