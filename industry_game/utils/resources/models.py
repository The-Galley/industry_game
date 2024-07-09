from dataclasses import dataclass
from enum import StrEnum, unique
from functools import cached_property


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
    amount: int

    @cached_property
    def icon(self) -> str:
        match self.type:
            case ResourceType.METALL:
                return "🔩"
            case ResourceType.CHEMICAL:
                return "🧪"
            case ResourceType.MACHINE:
                return "🚜"
            case ResourceType.LIGHT_INDUSTRY:
                return "🧵"
            case ResourceType.FOOD_INDUSTRY:
                return "🌾"
            case ResourceType.BITCOIN:
                return "💰"
            case _:
                return "?"
