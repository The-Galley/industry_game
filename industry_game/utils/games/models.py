from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, StringConstraints

from industry_game.db.models import Game as GameDb
from industry_game.db.models import GameStatus
from industry_game.utils.pagination import MetaPagination


@dataclass(frozen=True)
class Game:
    id: int
    name: str
    description: str
    created_by_id: int
    status: GameStatus
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, obj: GameDb) -> Self:
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            created_by_id=obj.created_by_id,
            status=obj.status,
            started_at=obj.started_at,
            finished_at=obj.finished_at,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class GameModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    created_by_id: int
    status: GameStatus
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    updated_at: datetime


class GamePaginationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    meta: MetaPagination
    items: list[GameModel]


class NewGameModel(BaseModel):
    name: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=128)
    ]
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=512)
    ]


class UpdateGameModel(BaseModel):
    name: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=128)
    ] | None = None
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=512)
    ] | None = None
