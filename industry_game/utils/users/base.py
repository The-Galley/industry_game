from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class UserType(StrEnum):
    ADMIN = "ADMIN"
    PLAYER = "PLAYER"


class RegisterPlayerModel(BaseModel):
    username: str = Field(min_length=8)
    password: str = Field(min_length=8)
    telegram: str = Field(min_length=2)
    name: str = Field(min_length=5)


class LoginUserModel(BaseModel):
    model_config = ConfigDict(str_min_length=8)

    username: str
    password: str


@dataclass(frozen=True)
class AuthUser:
    id: int
    username: str
    type: UserType

    def to_dict(self) -> dict[str, int | str]:
        return dict(id=self.id, username=self.username, type=self.type)


class AuthToken(BaseModel):
    token: str
