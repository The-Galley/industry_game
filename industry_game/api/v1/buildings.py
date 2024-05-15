from fastapi import APIRouter, Depends
from pydantic import Field

from industry_game.utils.buildings.models import BuildingPaginationModel
from industry_game.utils.buildings.storage import BuildingStorage
from industry_game.utils.http.auth.jwt import REQUIRE_ADMIN_AUTH
from industry_game.utils.overrides import GetBuildingStorage

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Depends(REQUIRE_ADMIN_AUTH)],
)


@router.get("")
async def get_list(
    limit: int = Field(default=20, gt=0, le=100),
    offset: int = Field(default=0, gt=-1),
    building_storage: BuildingStorage = Depends(GetBuildingStorage),
) -> BuildingPaginationModel:
    return await building_storage.pagination(limit=limit, offset=offset)


@router.post("")
async def create(
    new_building: CreateBuilidngModel,
    building_storage: BuildingStorage = Depends(GetBuildingStorage),
) -> BuildingModel:
    return await building_storage.create(new_building=new_building)
