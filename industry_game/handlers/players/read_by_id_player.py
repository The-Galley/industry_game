from aiohttp.web import HTTPForbidden, HTTPNotFound, Response, View

from industry_game.utils.http.auth.base import AuthMixin, require_authorization
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import parse_path_param
from industry_game.utils.http.response import msgspec_json_response
from industry_game.utils.users.base import UserType


class ReadByIdPlayerHandler(View, DependenciesMixin, AuthMixin):
    @require_authorization
    async def get(self) -> Response:
        player_id = parse_path_param(self.request, "player_id", int)

        if self.user.type != UserType.ADMIN and self.user.id != player_id:
            raise HTTPForbidden

        player = await self.player_storage.read_by_id(user_id=player_id)
        if player is None:
            raise HTTPNotFound
        return msgspec_json_response(player)
