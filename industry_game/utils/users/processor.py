from dataclasses import dataclass

from industry_game.utils.exceptions import (
    UserNotFoundException,
    UserWithUsernameAlreadExistsException,
)
from industry_game.utils.http.auth.jwt import JwtAuthrorizationProvider
from industry_game.utils.security import Passgen
from industry_game.utils.users.base import (
    AuthToken,
    AuthUserModel,
    RegisterPlayerModel,
)
from industry_game.utils.users.models import FullUser
from industry_game.utils.users.storage import PlayerStorage


@dataclass(frozen=True, slots=True)
class PlayerProcessor:
    player_storage: PlayerStorage
    passgen: Passgen
    jwt_provider: JwtAuthrorizationProvider

    async def register(self, player: RegisterPlayerModel) -> FullUser:
        if await self.player_storage.read_by_username(username=player.username):
            raise UserWithUsernameAlreadExistsException(
                username=player.username
            )
        return await self.player_storage.create(
            username=player.username,
            password_hash=self.passgen.hashpw(player.password),
        )

    async def login(self, player: AuthUserModel) -> AuthToken:
        user = await self.player_storage.get_by_username_and_password_hash(
            username=player.username,
            password_hash=self.passgen.hashpw(player.password),
        )
        if user is None:
            raise UserNotFoundException
        token = self.jwt_provider.generate_token(user=user)
        return AuthToken(token=token)
