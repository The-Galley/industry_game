from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    title: str
    message: str
