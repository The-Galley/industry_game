import logging
from dataclasses import dataclass

from industry_game.utils.events.base import AbstractEvent, EventStatus
from industry_game.utils.events.models import (
    BuildingEvent,
    GameContinueEvent,
    GamePauseEvent,
    ProductionEvent,
)
from industry_game.utils.events.storage import EventStorage

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class EventProcessor:
    event_storage: EventStorage

    async def process_event(self, event: AbstractEvent) -> None:
        try:
            if isinstance(event, BuildingEvent):
                await event.hook()
            elif isinstance(event, ProductionEvent):
                await event.hook()
            elif isinstance(event, GamePauseEvent):
                await event.hook()
            elif isinstance(event, GameContinueEvent):
                await event.hook()
            else:
                log.exception(
                    "Catch unkwnown event type of event %s",
                    event.model2dict(),
                )
                raise TypeError("Unknown Event type")
        except Exception:
            log.exception("Catch unhandled exception")
        else:
            await self.event_storage.update_status(
                event_uuid=event.uuid,
                status=EventStatus.FINISHED,
            )
