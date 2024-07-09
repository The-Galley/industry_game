from collections.abc import Mapping, MutableSequence, Sequence
from dataclasses import dataclass, field
from enum import StrEnum

from industry_game.utils.buildings.models import AbstractBuilding
from industry_game.utils.districts.models import District

HEIGHT = 10
WIDTH = 10


class HexagonState(StrEnum):
    EMPTY = "EMPTY"
    CAPTURING = "CAPTURING"
    CAPTURED = "CAPTURED"
    BUILDING = "BUILDING"
    BUILT = "BUILT"


@dataclass
class Hexagon:
    x: int
    y: int
    state: HexagonState = HexagonState.EMPTY
    building: AbstractBuilding | None = None
    district: District | None = None
    capturing_districts: MutableSequence[District] = field(default_factory=list)

    @property
    def is_captured(self) -> bool:
        return self.state == HexagonState.CAPTURED

    @property
    def is_built(self) -> bool:
        return self.state == HexagonState.BUILT

    def start_building(self, building: AbstractBuilding) -> None:
        self.building = building
        self.state = HexagonState.BUILDING

    def finish_building(self) -> None:
        self.state = HexagonState.BUILT

    @property
    def icon(self) -> str:
        match self.state:
            case HexagonState.EMPTY:
                return "empty"
            case HexagonState.BUILDING:
                return "🏗️"
            case HexagonState.BUILT:
                return "🏭"
            case HexagonState.CAPTURED:
                return "✅"
            case HexagonState.CAPTURING:
                return "♻️"
            case _:
                return "?"

    def is_capturing(self, district_id: int) -> bool:
        return any(d.id == district_id for d in self.capturing_districts)


class Map:
    _map: Sequence[Sequence[Hexagon]]
    _hexagons: Mapping[tuple[int, int], Hexagon]

    def __init__(self) -> None:
        self._map = [
            [Hexagon(x, y) for y in range(HEIGHT)] for x in range(WIDTH)
        ]
        self._hexagons = {
            (x, y): self._map[x][y] for x in range(WIDTH) for y in range(HEIGHT)
        }

    @property
    def width(self) -> int:
        return len(self._map)

    @property
    def height(self) -> int:
        return len(self._map[0])

    def capture_hexagon(self, x: int, y: int, district: District) -> None:
        hex = self._hexagons.get((x, y))
        if not hex:
            raise ValueError("Hexagon does not exist")
        hex.district = district
        hex.state = HexagonState.CAPTURED
        district.capture_hexagon(hex)

    @property
    def hexagons(self) -> Sequence[Sequence[Hexagon]]:
        return self._map
