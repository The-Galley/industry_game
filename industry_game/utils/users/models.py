import msgspec

from industry_game.db.models import User as UserDb
from industry_game.utils.msgspec import CustomStruct
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.base import UserType


class ShortUser(CustomStruct, frozen=True):
    id: int
    type: UserType
    username: str

    @classmethod
    def from_model(self, obj: UserDb) -> "ShortUser":
        return ShortUser(
            id=obj.id,
            type=obj.type,
            username=obj.username,
        )


class UserPagination(msgspec.Struct, frozen=True):
    meta: MetaPagination
    items: list[ShortUser]


class FullUser(CustomStruct, frozen=True):
    id: int
    type: UserType
    username: str

    @classmethod
    def from_model(self, obj: UserDb) -> "FullUser":
        return FullUser(
            id=obj.id,
            type=obj.type,
            username=obj.username,
        )
