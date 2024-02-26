import asyncio
import logging
from contextlib import suppress
from datetime import datetime, timedelta
from typing import Any

from aiomisc import Service

from industry_game.utils.events.models import AbstractEvent
from industry_game.utils.events.processor import EventProcessor
from industry_game.utils.typed import not_none

log = logging.getLogger(__name__)


class EventService(Service):
    event_queue: asyncio.Queue
    worker_task: asyncio.Task
    processor: EventProcessor

    async def start(self) -> Any:
        log.info("Start TimeEventWorker")
        self.worker_task = asyncio.create_task(self.work())
        self.start_event.set()

    async def stop(self, exception: Exception | None = None) -> Any:
        if self.worker_task and not self.worker_task.done():
            self.worker_task.cancel()
            with suppress(asyncio.CancelledError):
                await self.worker_task

    async def work(self) -> None:
        while True:
            event: AbstractEvent = await self.event_queue.get()
            log.debug("Got event: %s", event)
            if await self.is_rescheduled(event, datetime.now()):
                await self.event_queue.put(event)
            await self.process(event)
            await asyncio.sleep(0.01)

    async def is_rescheduled(self, event: AbstractEvent, now: datetime) -> bool:
        if event.game.is_paused:
            return True
        return (
            not_none(event.started_at) + timedelta(seconds=event.during_sec)
            < now
        )

    async def process(self, event: AbstractEvent) -> None:
        asyncio.shield(asyncio.create_task(self.processor.process_event(event)))
