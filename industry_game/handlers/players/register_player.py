from http import HTTPStatus

from aiohttp.web import HTTPBadRequest, HTTPConflict, Response, View
from pydantic import ValidationError

from industry_game.utils.exceptions import UserWithUsernameAlreadExistsException
from industry_game.utils.http.auth.base import AuthMixin
from industry_game.utils.http.auth.jwt import AUTH_COOKIE
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.response import msgspec_json_response
from industry_game.utils.users.base import RegisterPlayerModel


class RegisterPlayerHandler(View, DependenciesMixin, AuthMixin):
    async def post(self) -> Response:
        if self.user_or_none is not None:
            raise HTTPConflict(reason="You are already registered!")
        player = await self.parse_player_model()
        try:
            auth_token = await self.player_processor.register(player=player)
        except UserWithUsernameAlreadExistsException:
            raise HTTPBadRequest(
                reason="User with that username already exists"
            )
        response = msgspec_json_response(auth_token, status=HTTPStatus.CREATED)
        response.set_cookie(AUTH_COOKIE, auth_token.token)
        return response

    async def parse_player_model(self) -> RegisterPlayerModel:
        body = await self.request.read()
        try:
            return RegisterPlayerModel.model_validate_json(body)
        except ValidationError:
            raise HTTPBadRequest(reason="Incorrect input data")
