from http import HTTPStatus

from aiohttp.web import HTTPForbidden, HTTPNotFound, Response, View

from industry_game.db.models import GameStatus
from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_player_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_path_param


class DeleteUserFromLobbyHandler(View, DependenciesMixin, AuthMixin):
    @require_player_authorization
    async def delete(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)

        game = await self.game_storage.read_by_id(game_id=game_id)
        if game is None:
            raise HTTPNotFound
        if game.status != GameStatus.CREATED:
            raise HTTPForbidden
        await self.lobby_storage.delete(game_id=game_id, user_id=self.user.id)
        return Response(status=HTTPStatus.NO_CONTENT)
