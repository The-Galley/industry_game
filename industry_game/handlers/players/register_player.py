from http import HTTPStatus

from aiohttp.web import HTTPBadRequest, HTTPConflict, Response, View
from pydantic import ValidationError

from industry_game.utils.exceptions import UserWithUsernameAlreadExistsException
from industry_game.utils.http.auth.base import AuthMixin
from industry_game.utils.http.deps import DependenciesMixin
from industry_game.utils.http.response import msgspec_json_response
from industry_game.utils.users.base import RegisterPlayerModel


class RegisterPlayerHandler(View, DependenciesMixin, AuthMixin):
    async def post(self) -> Response:
        if self.user_or_none is not None:
            raise HTTPConflict(reason="You are already registered!")
        player = await self.parse_player_model()
        try:
            user = await self.player_processor.register(player=player)
        except UserWithUsernameAlreadExistsException:
            raise HTTPBadRequest(
                reason="User with that username already exists"
            )
        return msgspec_json_response(user, status=HTTPStatus.CREATED)

    async def parse_player_model(self) -> RegisterPlayerModel:
        body = await self.request.read()
        try:
            return RegisterPlayerModel.model_validate_json(body)
        except ValidationError:
            raise HTTPBadRequest
