from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    duration_seconds: int
    pause_seconds: int | None

    @property
    def is_last(self) -> bool:
        return self.pause_seconds is None


class SessionController:
    def __init__(self, sessions: Sequence[Session]):
        if len(sessions) == 0:
            raise ValueError("Sessions must not be empty")
        self._sessions = sessions
        self._session_index = 0

    @property
    def current_session(self) -> Session:
        return self._sessions[self._session_index]

    @property
    def is_last(self) -> bool:
        return self.current_session.is_last

    @property
    def is_first(self) -> bool:
        return self._session_index == 0

    def next(self) -> Session:
        self._session_index = (self._session_index + 1) % len(self._sessions)
        return self.current_session


SESSIONS = (
    Session(  # 1
        duration_seconds=10 * 60, pause_seconds=0
    ),
    Session(  # 2
        duration_seconds=10 * 60, pause_seconds=0
    ),
    Session(  # 3
        duration_seconds=9 * 60,
        pause_seconds=4 * 60,
    ),
    Session(  # 4
        duration_seconds=9 * 60,
        pause_seconds=0,
    ),
    Session(  # 5
        duration_seconds=9 * 60,
        pause_seconds=4 * 60,
    ),
    Session(  # 6
        duration_seconds=9 * 60,
        pause_seconds=0,
    ),
    Session(  # 7
        duration_seconds=9 * 60,
        pause_seconds=4 * 60,
    ),
    Session(  # 8
        duration_seconds=9 * 60,
        pause_seconds=0,
    ),
    Session(  # 9
        duration_seconds=12 * 60,
        pause_seconds=0,
    ),
    Session(  # 10
        duration_seconds=12 * 60,
        pause_seconds=None,
    ),
)
