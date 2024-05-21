from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from industry_game.utils.buildings.schemas import (
    BuildingModel,
    BuildingPaginationModel,
    CreateBuildingModel,
)
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
    limit: int = Query(default=20, gt=0, le=100),
    offset: int = Query(default=0, gt=-1),
    building_storage: BuildingStorage = Depends(GetBuildingStorage),
) -> BuildingPaginationModel:
    return await building_storage.pagination(limit=limit, offset=offset)


@router.post("")
async def create(
    new_building: CreateBuildingModel,
    building_storage: BuildingStorage = Depends(GetBuildingStorage),
) -> BuildingModel:
    return await building_storage.create(new_building=new_building)


@router.get("/{building_id}/")
async def get_by_id(
    building_id: int,
    building_storage: BuildingStorage = Depends(GetBuildingStorage),
) -> BuildingModel:
    building = await building_storage.get_by_id(building_id=building_id)
    if building is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Building not found",
        )
    return building
