from collections.abc import MutableSequence, Sequence
from enum import StrEnum, unique

from industry_game.utils.notifications.models import Notification


@unique
class PlayerRoles(StrEnum):
    DIRECTOR = "DIRECTOR"
    FINANCIER = "FINANCIER"
    HR_MANAGER = "HR_MANAGER"
    TERRITORY_MANAGER = "TERRITORY_MANAGER"
    DEVELOPER = "DEVELOPER"


class Player:
    _user_id: int
    _role: PlayerRoles
    _notifications: MutableSequence[Notification]

    def __init__(self, user_id: int, role: PlayerRoles) -> None:
        self._user_id = user_id
        self._role = role
        self._notifications = []

    def add_notification(self, notification: Notification) -> None:
        self._notifications.append(notification)

    @property
    def notifications(self) -> Sequence[Notification]:
        return self._notifications

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def role(self) -> PlayerRoles:
        return self._role
