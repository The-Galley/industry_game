from dataclasses import dataclass

from industry_game.utils.events.base import AbstractEvent


@dataclass
class BuildingEvent(AbstractEvent):
    pass


@dataclass
class ProductionEvent(AbstractEvent):
    pass


@dataclass
class GamePauseEvent(AbstractEvent):
    pass


@dataclass
class GameContinueEvent(AbstractEvent):
    pass
