from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

import msgspec
from pydantic import BaseModel, StringConstraints

from industry_game.db.models import Game as GameDb
from industry_game.db.models import GameStatus
from industry_game.utils.events.base import AbstractEvent
from industry_game.utils.games.session import SessionController
from industry_game.utils.maps.models import Hexagon
from industry_game.utils.pagination import MetaPagination


class GameResponse(msgspec.Struct, frozen=True):
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


class GamePaginationResponse(msgspec.Struct, frozen=True):
    meta: MetaPagination
    items: list[GameResponse]


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

    def from_model(self, obj: GameDb) -> "Game":
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


@dataclass
class MasterGame:
    game: Game
    session_controller: SessionController
    event_queue: deque[AbstractEvent]
    map: Mapping[tuple[int, int], Hexagon]
