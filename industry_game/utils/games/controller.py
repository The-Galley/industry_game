import logging
from collections import deque
from collections.abc import MutableMapping
from dataclasses import dataclass
from datetime import UTC, datetime

from industry_game.utils.events.base import AbstractEvent
from industry_game.utils.events.game import StartGameSessionEvent
from industry_game.utils.games.exceptions import GameNotFoundException
from industry_game.utils.games.models import Game, ProcessGame
from industry_game.utils.games.session import SESSIONS, SessionController
from industry_game.utils.games.storage import GameStorage

log = logging.getLogger(__name__)

START_GAME_DELAY = 3 * 60  # 3 minutes


@dataclass(frozen=True)
class GameController:
    game_storage: GameStorage
    current_games: MutableMapping[int, ProcessGame]
    event_queue: deque[AbstractEvent]

    async def start_game(self, game_id: int) -> None:
        game = await self.game_storage.get_by_id(game_id)
        if game is None:
            raise GameNotFoundException(game_id)
        self.add_new_game(
            game=game,
            event_queue=self.event_queue,
        )
        event = StartGameSessionEvent(
            game_id=game_id,
            delay=START_GAME_DELAY,
            created_at=datetime.now(tz=UTC),
            event_queue=self.event_queue,
            session_controller=self.current_games[game_id].session_controller,
            game_storage=self.game_storage,
        )
        self.event_queue.append(event)
        log.info("Game was %s started", game_id)

    def add_new_game(
        self,
        game: Game,
        event_queue: deque[AbstractEvent],
    ) -> None:
        self.current_games[game.id] = ProcessGame(
            game=game,
            event_queue=event_queue,
            session_controller=SessionController(sessions=SESSIONS),
        )
