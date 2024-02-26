import abc
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from industry_game.utils.games.models import Game


class EventType(StrEnum):
    BUILDING = "BUILDING"
    PRODUCTION = "PRODUCTION"


class EventStatus(StrEnum):
    CREATED = "CREATED"
    SCHEDULED = "SCHEDULED"
    FINISHED = "FINISHED"


@dataclass
class AbstractEvent(abc.ABC):
    uuid: UUID
    status: EventStatus
    type: EventType
    game: Game
    created_at: datetime
    started_at: datetime | None
    ended_at: datetime | None
    during_sec: int

    @property
    def properties(self) -> Mapping[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    async def hook(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def model2dict(self) -> Mapping[str, Any]:
        return {
            "uuid": self.uuid,
            "status": self.status,
            "type": self.type,
            "game_id": self.game.id,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "during_sec": self.during_sec,
            "properties": self.properties,
        }
