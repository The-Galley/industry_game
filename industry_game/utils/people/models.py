from collections.abc import Mapping, MutableMapping
from enum import StrEnum, unique


@unique
class HumanType(StrEnum):
    WORKER = "WORKER"
    SCIENTIST = "SCIENTIST"
    RESEARCHER = "RESEARCHER"


@unique
class HumanState(StrEnum):
    WORKING = "WORKING"
    RESTING = "RESTING"


class People:
    _people: Mapping[HumanType, MutableMapping[HumanState, int]]

    def __init__(self) -> None:
        self._people = {}
        for human_type in HumanType:
            self._people[human_type] = {hs: 0 for hs in HumanState}

    def set_working(self, human_type: HumanType, amount: int) -> None:
        self._subtract(human_type, HumanState.RESTING, amount)
        self.add(human_type, HumanState.WORKING, amount)

    def set_resting(self, human_type: HumanType, amount: int) -> None:
        self._subtract(human_type, HumanState.WORKING, amount)
        self.add(human_type, HumanState.RESTING, amount)

    def educate_workers(self, to: HumanType, amount: int) -> None:
        self._subtract(HumanType.WORKER, HumanState.WORKING, amount)
        self.add(to, HumanState.RESTING, amount)

    def has_empty_workers(self, worker_amount: int) -> bool:
        return (
            self._people[HumanType.WORKER][HumanState.RESTING] >= worker_amount
        )

    def add(
        self, human_type: HumanType, human_state: HumanState, amount: int
    ) -> None:
        self._people[human_type][human_state] += amount

    @property
    def value(self) -> Mapping[HumanType, Mapping[HumanState, int]]:
        return {
            human_type: {
                human_state: self._people[human_type][human_state]
                for human_state in HumanState
            }
            for human_type in HumanType
        }

    def _subtract(
        self, human_type: HumanType, human_state: HumanState, amount: int
    ) -> None:
        if self._people[human_type][human_state] < amount:
            raise ValueError("Not enough people")
        self._people[human_type][human_state] -= amount

    def init(self) -> None:
        for human_type, amount in (
            (HumanType.WORKER, 5),
            (HumanType.SCIENTIST, 1),
            (HumanType.RESEARCHER, 2),
        ):
            self._people[human_type][HumanState.RESTING] = amount
