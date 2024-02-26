from aiohttp.web import Response, View

from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_admin_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import (
    PaginationParamsModel,
    parse_query_params,
)
from industry_game.utils.http.response import msgspec_json_response


class ListGameHandler(View, DependenciesMixin, AuthMixin):
    @require_admin_authorization
    async def get(self) -> Response:
        page_params = parse_query_params(
            model=PaginationParamsModel,
            query=self.request.query,
        )
        game_pagination = await self.game_storage.pagination(
            page=page_params.page,
            page_size=page_params.page_size,
        )
        return msgspec_json_response(game_pagination)
