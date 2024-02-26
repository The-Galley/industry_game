from http import HTTPStatus

from aiohttp.web import Response, View

from industry_game.utils.games.models import NewGameModel
from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_admin_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_json_model
from industry_game.utils.http.response import msgspec_json_response


class CreateGameHandler(View, DependenciesMixin, AuthMixin):
    @require_admin_authorization
    async def post(self) -> Response:
        body = await self.request.read()
        new_game_data = parse_json_model(model=NewGameModel, data=body)

        game = await self.game_storage.create(
            name=new_game_data.name,
            description=new_game_data.description,
            created_by=self.user.id,
        )
        return msgspec_json_response(game, status=HTTPStatus.CREATED)
