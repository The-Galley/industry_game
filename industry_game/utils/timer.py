import asyncio
import time
from collections.abc import Awaitable


class Timer:
    _corouting: Awaitable
    _seconds: float
    _re_seconds: float
    _speed: float
    _start_time: float | None
    _stop_time: float | None
    _end_time: float | None
    _task: asyncio.Task | None

    def __init__(self, coroutine: Awaitable, seconds: float, speed: float = 1) -> None:
        self._coroutine = coroutine
        self._seconds = seconds
        self._re_seconds = seconds
        self._speed = speed

        self._start_time = None
        self._stop_time = None
        self._end_time = None
        self._task = None
        self._is_done = False

    def delay(self) -> None:
        self._task = asyncio.create_task(self._delay())

    @property
    def was_delayed(self) -> bool:
        return self._start_time is not None

    @property
    def re_seconds(self) -> float:
        elapsed_seconds = 0.0
        if self._stop_time and self._start_time:
            elapsed_seconds = (self._stop_time - self._start_time) * self._speed
        return self._re_seconds - elapsed_seconds

    async def _delay(self) -> None:
        if not self.was_delayed:
            self._start_time = time.monotonic()
        else:
            self._start_time = time.monotonic()
        await asyncio.sleep(self._re_seconds / self._speed)
        await asyncio.shield(self._coroutine)
        self._end_time = time.monotonic()

    def cancel(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        self._stop_time = time.monotonic()
        self._re_seconds = self.re_seconds
