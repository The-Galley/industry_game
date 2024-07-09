from __future__ import annotations

import abc
from collections.abc import Mapping, MutableMapping, Sequence, Set
from functools import cached_property
from typing import TYPE_CHECKING
from uuid import UUID

from industry_game.utils.approves.exceptions import ApproveNotFoundException
from industry_game.utils.approves.models import Approve
from industry_game.utils.buildings.models import (
    AbstractBuilding,
    ProductionResourceBuilding,
)
from industry_game.utils.districts.exceptions import (
    CannotBuildDistrictException,
    CannotProductionDistrictException,
)
from industry_game.utils.people.models import HumanType, People
from industry_game.utils.players.models import Player, PlayerRoles
from industry_game.utils.resources.balance import Balance
from industry_game.utils.resources.models import Resource

if TYPE_CHECKING:
    from industry_game.utils.maps.models import Hexagon


class District:
    _game_district_id: int
    _name: str
    _players: Mapping[PlayerRoles, Player]
    _balance: Balance
    _people: People
    _territory: MutableMapping[tuple[int, int], Hexagon]
    _approves: MutableMapping[UUID, Approve]

    def __init__(
        self, game_district_id: int, name: str, players: Sequence[Player]
    ) -> None:
        self._game_district_id = game_district_id
        self._name = name
        self._people = People()
        self._balance = Balance()
        self._players = {player.role: player for player in players}
        self._territory = {}
        self._approves = {}

    @property
    def id(self) -> int:
        return self._game_district_id

    @cached_property
    def users(self) -> Mapping[int, Player]:
        return {v.user_id: v for v in self._players.values()}

    @property
    def players(self) -> Mapping[PlayerRoles, Player]:
        return self._players

    @property
    def buildings(self) -> Mapping[int, AbstractBuilding]:
        return {
            h.building.id: h.building
            for h in self._territory.values()
            if h.building and h.is_built
        }

    def player_approves(self, player: Player) -> Mapping[UUID, Approve]:
        return {
            k: v
            for k, v in self._approves.items()
            if v.need_approve_from == player.role
        }

    def can_pay(self, resources: Set[Resource]) -> bool:
        return self._balance.can_pay(resources)

    def pay(self, resources: Set[Resource]) -> None:
        for resource in resources:
            self._balance.subtract(resource)

    def is_my_empty_territory(self, x: int, y: int) -> bool:
        hex = self._territory.get((x, y))
        if not hex:
            return False
        return hex.is_captured

    def start_building(
        self, x: int, y: int, building: AbstractBuilding
    ) -> None:
        self._territory[(x, y)].start_building(building)

    def finish_building(self, x: int, y: int) -> None:
        self._territory[(x, y)].finish_building()

    def has_empty_workers(self, worker_count: int) -> bool:
        return self._people.has_empty_workers(worker_count)

    def start_resource_production(self, building_id: int) -> None:
        building = self.buildings.get(building_id)
        if not building:
            raise CannotProductionDistrictException("Building not found")
        if not isinstance(building, ProductionResourceBuilding):
            raise CannotProductionDistrictException(
                "Building is not a resource building"
            )
        can_pay = self.can_pay(building.input)
        if not can_pay:
            raise CannotProductionDistrictException("Not enough resources")

        has_empty_workers = self.has_empty_workers(building.worker_count)
        if not has_empty_workers:
            raise CannotProductionDistrictException("Not enough workers")
        self._people.set_working(
            human_type=HumanType.WORKER, amount=building.worker_count
        )
        building.input_resources(self._balance)

    def finish_resource_production(self, building_id: int) -> None:
        building = self.buildings[building_id]
        if not isinstance(building, ProductionResourceBuilding):
            raise CannotProductionDistrictException(
                "Building is not a resource building"
            )
        self._people.set_resting(
            human_type=HumanType.WORKER, amount=building.worker_count
        )
        building.withdraw_output(self._balance)

    def capture_hexagon(self, hex: Hexagon) -> None:
        self._territory[(hex.x, hex.y)] = hex

    @property
    def name(self) -> str:
        return self._name

    @property
    def balance(self) -> Balance:
        return self._balance

    @property
    def people(self) -> People:
        return self._people

    async def approve(self, uuid: UUID) -> None:
        approve = self._approves.pop(uuid, None)
        if not approve:
            raise ApproveNotFoundException

        await approve.action.start()


class Action(abc.ABC):
    @abc.abstractmethod
    async def start(self) -> None:
        pass

    @abc.abstractmethod
    async def finish(self) -> None:
        pass


class BuildAction(Action):
    _district: District
    _building: AbstractBuilding
    _x: int
    _y: int

    def __init__(
        self, district: District, building: AbstractBuilding, x: int, y: int
    ) -> None:
        self._district = district
        self._building = building
        self._x = x
        self._y = y

    async def start(self) -> None:
        can_pay = self._district.can_pay(self._building.building_cost)
        if not can_pay:
            raise CannotBuildDistrictException("Not enough resources")
        has_empty_territory = self._district.is_my_empty_territory(
            self._x, self._y
        )
        if not has_empty_territory:
            raise CannotBuildDistrictException(
                "It's is not empty or not your territory"
            )

        self._district.pay(self._building.building_cost)
        self._district.start_building(self._x, self._y, self._building)

    async def finish(self) -> None:
        self._district.finish_building(self._x, self._y)


class ProductionResource(Action):
    _district: District
    _building_id: int

    def __init__(self, district: District, building_id: int) -> None:
        self._building_id = building_id
        self._district = district

    async def start(self) -> None:
        self._district.start_resource_production(self._building_id)

    async def finish(self) -> None:
        self._district.finish_resource_production(self._building_id)
