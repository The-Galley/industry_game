from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class NotificationTargetType(StrEnum):
    ALL = "ALL"
    DISTRICT = "DISTRICT"
    PLAYER = "PLAYER"


@dataclass
class NotificationTarget:
    target_type: NotificationTargetType
    object_id: int


@dataclass
class Notification:
    targets: Sequence[NotificationTarget]
    message_template: str

    def message(self, **kwargs: Any) -> str:
        return self.message_template.format(**kwargs)
