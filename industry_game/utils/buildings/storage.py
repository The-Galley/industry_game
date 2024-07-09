import asyncio
from collections.abc import Sequence

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Building as BuildingDb
from industry_game.utils.buildings.schemas import (
    BuildingModel,
    BuildingPaginationModel,
    CreateBuildingModel,
)
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.pagination import MetaPagination


class BuildingStorage(AbstractStorage):
    async def pagination(
        self, limit: int, offset: int
    ) -> BuildingPaginationModel:
        total, items = await asyncio.gather(
            self._get_count(),
            self._get_items(limit=limit, offset=offset),
        )
        return BuildingPaginationModel(
            meta=MetaPagination(
                total=total,
            ),
            items=items,
        )

    @inject_session
    async def create(
        self, *, session: AsyncSession, model: CreateBuildingModel
    ) -> BuildingModel:
        stmt = (
            insert(BuildingDb)
            .values(**model.model_dump(mode="python"))
            .returning(BuildingDb)
        )
        result = await session.scalars(stmt)
        return BuildingModel.model_validate(result.one())

    @inject_session
    async def get_by_id(
        self, *, session: AsyncSession, building_id: int
    ) -> BuildingModel | None:
        building = await session.get(BuildingDb, building_id)
        return BuildingModel.model_validate(building) if building else None

    @inject_session
    async def _get_count(self, *, session: AsyncSession) -> int:
        query = select(func.count()).select_from(select(BuildingDb).subquery())
        return (await session.execute(query)).scalar_one()

    @inject_session
    async def _get_items(
        self,
        *,
        session: AsyncSession,
        limit: int,
        offset: int,
    ) -> Sequence[BuildingDb]:
        query = (
            select(BuildingDb)
            .limit(limit)
            .offset(offset)
            .order_by(BuildingDb.id)
        )
        return (await session.execute(query)).scalars().all()
