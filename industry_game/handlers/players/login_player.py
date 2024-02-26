from http import HTTPStatus

from aiohttp.web import (
    HTTPBadRequest,
    HTTPConflict,
    HTTPNotFound,
    Response,
    View,
)
from pydantic import ValidationError

from industry_game.utils.exceptions import UserNotFoundException
from industry_game.utils.http.auth.base import AuthMixin
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.response import msgspec_json_response
from industry_game.utils.users.base import AuthUserModel


class LoginPlayerHandler(View, DependenciesMixin, AuthMixin):
    async def post(self) -> Response:
        if self.user_or_none is not None:
            raise HTTPConflict(reason="You are already logined")
        player = await self.parse_player_model()
        try:
            auth_token = await self.player_processor.login(player=player)
        except UserNotFoundException:
            raise HTTPNotFound(
                reason="User with that username and password not found"
            )
        return msgspec_json_response(auth_token, status=HTTPStatus.OK)

    async def parse_player_model(self) -> AuthUserModel:
        body = await self.request.read()
        try:
            return AuthUserModel.model_validate_json(body)
        except ValidationError:
            raise HTTPBadRequest
