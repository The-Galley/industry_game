from dataclasses import dataclass

from industry_game.utils.buildings.models import Building


@dataclass(frozen=True, slots=True)
class NotificationProcessor:
    async def notify_about_building(self, building: Building) -> None:
        pass

    async def notify_about_production(self, building: Building) -> None:
        pass
