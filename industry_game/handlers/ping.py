import logging
from http import HTTPStatus

from aiohttp.web import Response, View
from aiomisc import timeout
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.response import fast_json_response

log = logging.getLogger(__name__)


class PingHandler(View, DependenciesMixin):
    async def get(self) -> Response:
        try:
            db = await self._ping()
        except TimeoutError:
            db = False
        deps = {
            "db": db,
        }
        if all(deps.values()):
            status_code = HTTPStatus.OK
        else:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return fast_json_response(
            data=deps,
            status=status_code,
        )

    @timeout(1)
    async def _ping(self) -> bool:
        try:
            async with self.session_factory() as session:
                await session.execute(text("select 1"))
                return True
        except SQLAlchemyError:
            return False
