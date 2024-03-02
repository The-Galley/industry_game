from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from industry_game.utils.msgspec import CustomStruct


class UserType(StrEnum):
    ADMIN = "ADMIN"
    PLAYER = "PLAYER"


class RegisterPlayerModel(BaseModel):
    username: str = Field(min_length=8)
    password: str = Field(min_length=8)
    telegram: str = Field(min_length=2)
    name: str = Field(min_length=5)


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
