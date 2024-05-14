from dataclasses import dataclass
from enum import StrEnum, unique

import msgspec


@unique
class ResourceType(StrEnum):
    METALL = "METALL"
    CHEMICAL = "CHEMICAL"
    MACHINE = "MACHINE"
    LIGHT_INDUSTRY = "LIGHT_INDUSTRY"
    FOOD_INDUSTRY = "FOOD_INDUSTRY"
    BITCOIN = "BITCOIN"


@dataclass(frozen=True)
class Resource:
    type: ResourceType
    count: int


class ResourceStruct(msgspec.Struct, frozen=True):
    type: ResourceType
    count: int
