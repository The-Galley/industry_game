import msgspec

from industry_game.utils.games.models import Game


class BuildingType:
    pass


class Building:
    type: BuildingType
    game: Game


class BuildingTypeStruct(msgspec.Struct, frozen=True):
    name: str


class BuildingStruct(msgspec.Struct, frozen=True):
    type: BuildingType
    game_id: int
