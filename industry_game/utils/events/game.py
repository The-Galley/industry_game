import logging
from collections import deque
from datetime import UTC, datetime
from uuid import UUID

from industry_game.db.models import GameStatus
from industry_game.utils.events.base import AbstractEvent, EventStatus
from industry_game.utils.games.session import SessionController
from industry_game.utils.games.storage import GameStorage

log = logging.getLogger(__name__)


class StartGameSessionEvent(AbstractEvent):
    _event_queue: deque[AbstractEvent]
    _session_controller: SessionController
    _game_storage: GameStorage

    def __init__(
        self,
        uuid: UUID,
        game_id: int,
        delay: int,
        created_at: datetime,
        event_queue: deque[AbstractEvent],
        session_controller: SessionController,
        game_storage: GameStorage,
        name: str = "StartGameSessionEvent",
        speed: float = 1.0,
        is_active: bool = True,
    ) -> None:
        super().__init__(
            uuid=uuid,
            name=name,
            game_id=game_id,
            delay=delay,
            created_at=created_at,
            speed=speed,
            is_active=is_active,
        )
        self._event_queue = event_queue
        self._session_controller = session_controller
        self._game_storage = game_storage

    async def pre_hook(self) -> None:
        return

    async def execute(self) -> None:
        await self._game_storage.update_status(
            game_id=self._game_id,
            status=GameStatus.STARTED,
        )
        now = datetime.now(UTC)
        for event in self._event_queue:
            if event.game_id == self.game_id and not event.is_active:
                event.set_status(EventStatus.SCHEDULED)
                event.set_last_updated_at(dt=now)

    async def post_hook(self) -> None:
        self._event_queue.append(
            EndGameSessionEvent(
                delay=self._session_controller.current_session.duration_seconds,
                game_id=self.game_id,
                event_queue=self._event_queue,
                session_controller=self._session_controller,
            )
        )


class EndGameSessionEvent(AbstractEvent):
    _event_queue: deque[AbstractEvent]
    _session_controller: SessionController

    def __init__(
        self,
        uuid: UUID,
        event_queue: deque[AbstractEvent],
        session_controller: SessionController,
        game_id: int,
        delay: int,
        created_at: datetime,
        speed: float,
        is_active: bool,
        name: str = "StopGameSessionEvent",
    ) -> None:
        super().__init__(
            uuid=uuid,
            name=name,
            game_id=game_id,
            delay=delay,
            created_at=created_at,
            speed=speed,
            is_active=is_active,
        )
        self._event_queue = event_queue
        self._session_controller = session_controller

    async def pre_hook(self) -> None:
        pass

    async def execute(self) -> None:
        for event in self._event_queue:
            if event.game_id == self.game_id and event.is_active:
                event.set_status(EventStatus.PAUSED)

    async def post_hook(self) -> None:
        if self._session_controller.is_last:
            while self._event_queue:
                event = self._event_queue.popleft()
                log.info("event %s was destroyed before finished", event)
        else:
            next_session = self._session_controller.next()
            self._event_queue.append(
                StartGameSessionEvent(
                    delay=next_session.pause_seconds,
                    game_id=self._game_id,
                    event_queue=self._event_queue,
                    session_controller=self._session_controller,
                )
            )


class PauseGameSessionEvent(AbstractEvent):
    _event_queue: deque[AbstractEvent]

    def __init__(
        self,
        event_queue: deque[AbstractEvent],
        game_id: int,
        delay: int,
        created_at: datetime,
        speed: float,
        is_active: bool,
        name: str = "PauseGameSessionEvent",
    ) -> None:
        self._event_queue = event_queue
        super().__init__(
            name=name,
            game_id=game_id,
            delay=delay,
            created_at=created_at,
            speed=speed,
            is_active=is_active,
        )

    async def pre_hook(self) -> None:
        pass

    async def execute(self) -> None:
        for event in self._event_queue:
            if event.game_id == self.game_id and event.is_active:
                event.set_status(EventStatus.PAUSED)

    async def post_hook(self) -> None:
        pass
