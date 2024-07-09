from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from industry_game.utils.districts.models import Action
    from industry_game.utils.players.models import PlayerRoles


class ApproveMessages(StrEnum):
    NEW_BUILDING = "Требуется подтверждение строительства"
    NEW_PRODUCTION = "Требуется подтверждение снабжения"


@dataclass(frozen=True)
class Approve:
    uuid: UUID
    message: ApproveMessages
    action: Action
    need_approve_from: PlayerRoles
    created_at: datetime = field(default_factory=datetime.now)
