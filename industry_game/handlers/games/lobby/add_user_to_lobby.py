from http import HTTPStatus

from aiohttp.web import HTTPForbidden, HTTPNotFound, Response, View

from industry_game.db.models import GameStatus
from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_player_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_path_param


class AddUserToGameLobbyHandler(View, DependenciesMixin, AuthMixin):
    @require_player_authorization
    async def post(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)

        game = await self.game_storage.read_by_id(game_id=game_id)
        if game is None:
            raise HTTPNotFound
        if game.status != GameStatus.CREATED:
            raise HTTPForbidden
        lobby = await self.lobby_storage.read_by_id(
            game_id=game_id, user_id=self.user.id
        )
        if lobby is not None:
            return Response(status=HTTPStatus.OK)

        await self.lobby_storage.add_user(game_id=game_id, user_id=self.user.id)
        return Response(status=HTTPStatus.CREATED)
