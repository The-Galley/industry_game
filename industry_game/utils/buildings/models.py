import abc
from collections.abc import Set
from dataclasses import dataclass

from industry_game.db.models import BuildingLevel
from industry_game.utils.resources.balance import Balance
from industry_game.utils.resources.models import Resource


class AbstractBuilding(abc.ABC):
    id: int
    name: str
    description: str
    category: str
    level: BuildingLevel
    building_cost: Set[Resource]
    building_time_sec: int
    icon: str | None = None


@dataclass(frozen=True)
class ProductionResourceBuilding(AbstractBuilding):
    id: int
    name: str
    description: str
    category: str
    level: BuildingLevel
    building_cost: Set[Resource]
    building_time_sec: int
    input: Set[Resource]
    output: Set[Resource]
    worker_count: int
    process_time_sec: int
    icon: str | None

    def input_resources(self, balance: Balance) -> None:
        for resource in self.input:
            balance.subtract(resource)

    def withdraw_output(self, balance: Balance) -> None:
        for resource in self.output:
            balance.add(resource)
