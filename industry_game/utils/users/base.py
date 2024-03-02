from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from industry_game.utils.msgspec import CustomStruct


class UserType(StrEnum):
    ADMIN = "ADMIN"
    PLAYER = "PLAYER"


class RegisterPlayerModel(BaseModel):
    username: str
    password: str


class AuthUserModel(BaseModel):
    model_config = ConfigDict(str_min_length=8)

    username: str
    password: str


class AuthUser(CustomStruct, frozen=True):
    id: int
    username: str
    type: UserType


class AuthToken(CustomStruct, frozen=True):
    token: str
