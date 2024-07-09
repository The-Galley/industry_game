import abc
from collections.abc import Sequence, Set
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, RootModel

from industry_game.db.models import BuildingLevel, BuildingType
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.people.schemas import HumanModel
from industry_game.utils.resources.schemas import ResourceModel


class BaseBuildingModel(BaseModel, abc.ABC):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    category: str
    icon: str | None = None
    level: BuildingLevel


class PeopleProductionPropertiesModel(BaseModel):
    build_cost: Sequence[ResourceModel]
    input: Sequence[ResourceModel]
    output: Sequence[HumanModel]
    building_time_sec: PositiveInt
    process_time_sec: PositiveInt


class PeopleEducationPropertiesModel(BaseModel):
    build_cost: Set[ResourceModel]
    input_people: Set[HumanModel]
    input_resource: Set[ResourceModel]
    output: Set[HumanModel]
    building_time_sec: PositiveInt
    process_time_sec: PositiveInt


class ResourceProductionPropertiesModel(BaseModel):
    build_cost: Set[ResourceModel]
    building_time_sec: PositiveInt
    worker_count: PositiveInt
    input: Set[ResourceModel]
    process_time_sec: PositiveInt
    output: Set[ResourceModel]


class CreatePeopleProductionBuildingModel(BaseBuildingModel):
    type: Literal[BuildingType.PEOPLE_PRODUCTION]
    properties: PeopleProductionPropertiesModel


class CreatePeopleEducationBuildingModel(BaseBuildingModel):
    type: Literal[BuildingType.PEOPLE_EDUCATION]
    properties: PeopleEducationPropertiesModel


class CreateResourceProductionBuildingModel(BaseBuildingModel):
    type: Literal[BuildingType.RESOURCE_PRODUCTION]
    properties: ResourceProductionPropertiesModel


class CreateBuildingModel(RootModel):
    root: Annotated[
        CreatePeopleEducationBuildingModel
        | CreatePeopleProductionBuildingModel
        | CreateResourceProductionBuildingModel,
        Field(discriminator="type"),
    ]


class PeopleProductionBuildingModel(BaseBuildingModel):
    id: int
    type: Literal[
        BuildingType.PEOPLE_PRODUCTION
    ] = BuildingType.PEOPLE_PRODUCTION
    properties: PeopleProductionPropertiesModel


class PeopleEducationBuildingModel(BaseBuildingModel):
    id: int
    type: Literal[BuildingType.PEOPLE_EDUCATION] = BuildingType.PEOPLE_EDUCATION
    properties: PeopleEducationPropertiesModel


class ResourceProductionBuildingModel(BaseBuildingModel):
    id: int
    type: Literal[
        BuildingType.RESOURCE_PRODUCTION
    ] = BuildingType.RESOURCE_PRODUCTION
    properties: ResourceProductionPropertiesModel


class BuildingModel(RootModel):
    root: Annotated[
        PeopleEducationBuildingModel
        | PeopleProductionBuildingModel
        | ResourceProductionBuildingModel,
        Field(discriminator="type"),
    ]


class ShortBuildingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    type: BuildingType
    category: str
    level: BuildingLevel
    icon: str | None


class BuildingPaginationModel(BaseModel):
    items: list[ShortBuildingModel]
    meta: MetaPagination
