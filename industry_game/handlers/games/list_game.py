from aiohttp.web import Response, View

from industry_game.db.models import GameStatus
from industry_game.utils.http.auth.base import (
    AuthMixin,
    require_authorization,
)
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.params import (
    PaginationParamsModel,
    parse_query_params,
)
from industry_game.utils.http.response import msgspec_json_response
from industry_game.utils.users.base import UserType


class ListGameHandler(View, DependenciesMixin, AuthMixin):
    @require_authorization
    async def get(self) -> Response:
        page_params = parse_query_params(
            model=PaginationParamsModel,
            query=self.request.query,
        )
        if self.user.type == UserType.ADMIN:
            game_pagination = await self.game_storage.pagination(
                page=page_params.page,
                page_size=page_params.page_size,
            )
        else:
            game_pagination = await self.game_storage.pagination(
                page=page_params.page,
                page_size=page_params.page_size,
                status=GameStatus.CREATED,
            )
        return msgspec_json_response(game_pagination)
