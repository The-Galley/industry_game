import asyncio
import logging
from collections import deque
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from aiomisc import Service

from industry_game.utils.events.base import MAX_EVENT_PROGRESS
from industry_game.utils.events.models import AbstractEvent
from industry_game.utils.events.processor import EventProcessor

log = logging.getLogger(__name__)


class EventService(Service):
    event_queue: deque[AbstractEvent]
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
            if not self.event_queue:
                continue
            event = self.event_queue.popleft()
            log.debug("Got event: %s", event)
            now = datetime.now(tz=UTC)
            if event.is_active:
                event.update_progress(now=now)
                if event.progress >= MAX_EVENT_PROGRESS:
                    self.process(event)
                else:
                    self.event_queue.append(event)
            await asyncio.sleep(0.01)

    def process(self, event: AbstractEvent) -> None:
        task = asyncio.shield(asyncio.create_task(event.execute()))
        task.add_done_callback(event.post_hook())
