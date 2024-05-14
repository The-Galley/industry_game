from collections.abc import Mapping
from dataclasses import dataclass

import msgspec

from industry_game.utils.buildings.models import Building, BuildingStruct
from industry_game.utils.districts.models import District, DistrictStruct
from industry_game.utils.resources.models import Resource, ResourceStruct


class HexagonStruct(msgspec.Struct, frozen=True):
    x: int
    y: int
    building: BuildingStruct | None = None
    district: DistrictStruct | None = None
    resource: ResourceStruct | None = None


@dataclass
class Hexagon:
    x: int
    y: int
    building: Building | None
    district: District | None
    resource: Resource | None


@dataclass(frozen=True)
class HexagonMap:
    map: Mapping[tuple[int, int], Hexagon]
