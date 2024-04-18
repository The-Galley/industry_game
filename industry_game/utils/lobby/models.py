from enum import StrEnum, unique

from pydantic import BaseModel, ConfigDict

from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.models import ShortUserModel


class LobbyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    game_id: int
    user_id: int


class LobbyPaginationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meta: MetaPagination
    items: list[ShortUserModel]


@unique
class LobbyStatusType(StrEnum):
    CHECKED_IN = "CHECKED_IN"
    NOT_CHECKED_IN = "NOT_CHECKED_IN"


class LobbyStatus(BaseModel):
    status: StrEnum
