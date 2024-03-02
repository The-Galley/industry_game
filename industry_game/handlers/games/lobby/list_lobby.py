from aiohttp.web import HTTPNotFound, Response, View

from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_admin_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import (
    PaginationParamsModel,
    parse_path_param,
    parse_query_params,
)
from industry_game.utils.http.response import msgspec_json_response


class ListGameLobbyHandler(View, DependenciesMixin, AuthMixin):
    @require_admin_authorization
    async def get(self) -> Response:
        game_id = parse_path_param(self.request, "game_id", int)
        game = await self.game_storage.read_by_id(game_id=game_id)
        if game is None:
            raise HTTPNotFound
        page_params = parse_query_params(
            model=PaginationParamsModel,
            query=self.request.query,
        )
        lobby_pagination = await self.lobby_storage.pagination(
            game_id=game_id,
            page=page_params.page,
            page_size=page_params.page_size,
        )
        return msgspec_json_response(lobby_pagination)
