from enum import StrEnum, unique

import msgspec

from industry_game.db.models import UserGameLobby as UserGameLobbyDb
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.models import ShortUser


class Lobby(msgspec.Struct, frozen=True):
    game_id: int
    user_id: int

    @classmethod
    def from_model(cls, obj: UserGameLobbyDb) -> "Lobby":
        return Lobby(
            game_id=obj.game_id,
            user_id=obj.user_id,
        )


class LobbyPagination(msgspec.Struct, frozen=True):
    meta: MetaPagination
    items: list[ShortUser]


@unique
class LobbyStatusType(StrEnum):
    CHECKED_IN = "CHECKED_IN"
    NOT_CHECKED_IN = "NOT_CHECKED_IN"


class LobbyStatus(msgspec.Struct, frozen=True):
    status: StrEnum
