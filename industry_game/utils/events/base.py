import abc
from datetime import datetime
from enum import StrEnum, unique
from typing import Any
from uuid import UUID

MAX_EVENT_PROGRESS = 1


@unique
class EventType(StrEnum):
    BUILDING = "BUILDING"
    PRODUCTION = "PRODUCTION"


@unique
class EventStatus(StrEnum):
    CREATED = "CREATED"
    SCHEDULED = "SCHEDULED"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"


class AbstractEvent(abc.ABC):
    _uuid: UUID
    _created_at: datetime
    _delay: int
    _finished_at: datetime | None
    _is_active: bool
    _last_updated_at: datetime
    _status: EventStatus
    _progress: float

    _name: str
    _game_id: int

    def __init__(
        self,
        uuid: UUID,
        name: str,
        game_id: int,
        delay: int,
        created_at: datetime,
        speed: float,
        is_active: bool,
    ) -> None:
        self._uuid = uuid
        self._name = name
        self._game_id = game_id
        self._created_at = created_at
        self._delay = delay
        self._finished_at = None
        self._is_active = is_active
        self._last_updated_at = created_at
        self._progress = 0
        self._speed = speed
        self._status = EventStatus.CREATED

    def __repr__(self) -> str:
        return self._name

    @property
    def progress(self) -> float:
        return self._progress

    @property
    def game_id(self) -> int:
        return self._game_id

    @property
    def uuid(self) -> UUID:
        return self._uuid

    def update_progress(self, dt: datetime) -> None:
        new_progres = (
            self._progress
            + (dt - self._last_updated_at).total_seconds()
            / self._delay
            * self._speed
        )
        self._progress = min(MAX_EVENT_PROGRESS, new_progres)

    def set_last_updated_at(self, dt: datetime) -> None:
        self._last_updated_at = dt

    def set_status(self, status: EventStatus) -> None:
        self._status = status

    @abc.abstractmethod
    async def pre_hook(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def post_hook(self) -> None:
        raise NotImplementedError

    def is_active(self) -> bool:
        return self._is_active

    def model2dict(self) -> dict[str, Any]:
        return {
            "name": self._name,
            "game_id": self._game_id,
            "created_at": self._created_at,
            "delay": self._delay,
            "finished_at": self._finished_at,
            "is_active": self._is_active,
            "last_updated_at": self._last_updated_at,
            "status": self._status,
            "progress": self._progress,
        }
