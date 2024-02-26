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


class ListPlayerHandler(View, DependenciesMixin, AuthMixin):
    @require_admin_authorization
    async def get(self) -> Response:
        page_params = parse_query_params(
            model=PaginationParamsModel,
            query=self.request.query,
        )
        user_pagination = await self.player_storage.pagination(
            page=page_params.page,
            page_size=page_params.page_size,
        )
        return msgspec_json_response(user_pagination)
