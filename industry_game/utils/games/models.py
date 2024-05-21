from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, StringConstraints

from industry_game.db.models import Game as GameDb
from industry_game.db.models import GameStatus
from industry_game.utils.districts.models import District
from industry_game.utils.events.base import AbstractEvent
from industry_game.utils.games.session import Session, SessionController
from industry_game.utils.maps.models import Map
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.players.models import Player


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


class ProcessGame:
    def __init__(
        self,
        game: Game,
        event_queue: deque[AbstractEvent],
        session_controller: SessionController,
        districts: Mapping[int, District],
        map: Map,
    ) -> None:
        self._game = game
        self._event_queue = event_queue
        self._session_controller = session_controller
        self._districts = districts
        self._map = map

    @cached_property
    def players(self) -> Mapping[int, Player]:
        return {
            v.user_id: v
            for d in self._districts.values()
            for v in d.players.values()
        }

    @property
    def districts(self) -> Mapping[int, District]:
        return self._districts

    @cached_property
    def player_districts(self) -> Mapping[int, District]:
        return {
            v.user_id: d
            for d in self._districts.values()
            for v in d.players.values()
        }

    def init_territories(
        self, district_hex: Mapping[tuple[int, int], int]
    ) -> None:
        for (x, y), district_id in district_hex.items():
            self._map.capture_hexagon(x, y, self._districts[district_id])

    @property
    def current_session(self) -> Session:
        return self._session_controller.current_session

    @property
    def name(self) -> str:
        return self._game.name

    @property
    def description(self) -> str:
        return self._game.description

    @property
    def map(self) -> Map:
        return self._map

    @property
    def session_controller(self) -> SessionController:
        return self._session_controller
