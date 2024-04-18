from dataclasses import dataclass

from industry_game.utils.exceptions import (
    UserWithUsernameAlreadExistsException,
)
from industry_game.utils.http.auth.jwt import JwtAuthProvider
from industry_game.utils.security import Passgen
from industry_game.utils.users.base import (
    AuthToken,
    LoginUserModel,
    RegisterPlayerModel,
)
from industry_game.utils.users.storage import UserStorage


@dataclass(frozen=True, slots=True)
class LoginProvider:
    user_storage: UserStorage
    passgen: Passgen
    auth_provider: JwtAuthProvider

    async def register_player(self, player: RegisterPlayerModel) -> AuthToken:
        if await self.user_storage.read_by_username(username=player.username):
            raise UserWithUsernameAlreadExistsException(
                username=player.username
            )
        user = await self.user_storage.create(
            username=player.username,
            password_hash=self.passgen.hashpw(player.password),
            properties={
                "telegram": player.telegram,
                "name": player.name,
            },
        )
        token = self.auth_provider.generate_token(user=user)
        return AuthToken(token=token)

    async def login(self, login_user: LoginUserModel) -> AuthToken | None:
        user = await self.user_storage.get_by_username_and_password_hash(
            username=login_user.username,
            password_hash=self.passgen.hashpw(login_user.password),
        )
        if user is None:
            return None
        token = self.auth_provider.generate_token(user=user)
        return AuthToken(token=token)
