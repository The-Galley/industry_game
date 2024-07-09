from collections.abc import Callable

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Building, BuildingLevel, BuildingType
from industry_game.utils.buildings.models import (
    PeopleModel,
    PeopleProductionPropertiesModel,
    ResourceModel,
)
from industry_game.utils.resources.models import PeopleType, ResourceType


class PeopleProductionPropertiesFactory(factory.Factory):
    class Meta:
        model = PeopleProductionPropertiesModel

    build_cost = [ResourceModel(resource=ResourceType.BITCOIN, amount=10)]
    input = [ResourceModel(resource=ResourceType.FOOD_INDUSTRY, amount=1)]
    output = [PeopleModel(resource=PeopleType.PEOPLE, amount=1)]


class BuildingFactory(factory.Factory):
    class Meta:
        model = Building

    id: int = factory.Sequence(lambda n: n + 1)
    name: str = "New building"
    type: BuildingType = BuildingType.RESOURCE_PRODUCTION
    description: str = "New building description"
    icon: str | None = None
    category: str = "category"
    level: BuildingLevel = BuildingLevel.FIRST
    properties: dict


@pytest.fixture
def create_building(session: AsyncSession) -> Callable:
    async def _create(**kwargs) -> Building:
        building = BuildingFactory(**kwargs)
        session.add(building)
        await session.commit()
        await session.flush(building)
        return building

    return _create
