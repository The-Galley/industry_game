import msgspec
from pydantic import BaseModel, ConfigDict

from industry_game.utils.games.models import Game
from industry_game.utils.pagination import MetaPagination


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


class BuildingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class ShortBuildingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class BuildingPaginationModel(BaseModel):
    items: list[ShortBuildingModel]
    meta: MetaPagination
