import logging
from collections import defaultdict
from collections.abc import Mapping, MutableMapping, Sequence, Set

from industry_game.utils.resources.models import Resource, ResourceType

log = logging.getLogger(__name__)

INIT_RESOURCES = (
    Resource(type=ResourceType.BITCOIN, amount=100),
    Resource(type=ResourceType.CHEMICAL, amount=80),
    Resource(type=ResourceType.FOOD_INDUSTRY, amount=60),
    Resource(type=ResourceType.LIGHT_INDUSTRY, amount=40),
    Resource(type=ResourceType.MACHINE, amount=20),
    Resource(type=ResourceType.METALL, amount=0),
)


class Balance:
    _resources: MutableMapping[ResourceType, int]

    def __init__(self) -> None:
        self._resources = defaultdict(int)

    def add(self, resource: Resource) -> None:
        log.info("add resource %s", resource)
        self._resources[resource.type] += resource.amount

    def subtract(self, resource: Resource) -> None:
        if self._resources[resource.type] < resource.amount:
            raise ValueError("Not enough resources")
        self._resources[resource.type] -= resource.amount

    @property
    def value(self) -> Mapping[ResourceType, int]:
        return {k: v for k, v in self._resources.items()}

    def can_pay(self, resources: Set[Resource]) -> bool:
        return all(
            self._resources.get(resource.type, 0) >= resource.amount
            for resource in resources
        )

    @property
    def resources(self) -> Sequence[Resource]:
        return [Resource(k, v) for k, v in self._resources.items()]

    def init(self) -> None:
        for resource in INIT_RESOURCES:
            self.add(resource)
