from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Self

from pydantic import BaseModel, ConfigDict

from industry_game.db.models import User as UserDb
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.base import UserType


@dataclass(frozen=True)
class User:
    id: int
    type: UserType
    username: str
    properties: Mapping[str, str]

    @classmethod
    def from_model(cls, obj: UserDb) -> Self:
        return cls(
            id=obj.id,
            type=obj.type,
            username=obj.username,
            properties=obj.properties,
        )

    @property
    def telegram(self) -> str:
        return self.properties.get("telegram", "")

    @property
    def name(self) -> str:
        return self.properties.get("name", "")


class ShortUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: UserType
    username: str


class FullUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: UserType
    username: str
    telegram: str
    name: str


class UserPaginationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meta: MetaPagination
    items: Sequence[ShortUserModel]
