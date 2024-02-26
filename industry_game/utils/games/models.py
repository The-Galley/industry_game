from datetime import datetime
from typing import Annotated

import msgspec
from pydantic import BaseModel, StringConstraints

from industry_game.db.models import Game as GameDb
from industry_game.db.models import GameStatus
from industry_game.utils.pagination import MetaPagination


class Game(msgspec.Struct, frozen=True):
    id: int
    name: str
    description: str
    created_by_id: int
    status: GameStatus
    started_at: datetime | None
    finished_at: datetime | None
    created_at: Annotated[datetime, msgspec.Meta(tz=False)]
    updated_at: Annotated[datetime, msgspec.Meta(tz=False)]

    @property
    def is_paused(self) -> bool:
        return self.status == GameStatus.PAUSED

    @classmethod
    def from_model(cls, obj: GameDb) -> "Game":
        return Game(
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


class GamePagination(msgspec.Struct, frozen=True):
    meta: MetaPagination
    items: list[Game]


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
