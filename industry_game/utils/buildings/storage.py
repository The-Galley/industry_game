import asyncio
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Building as BuildingDb
from industry_game.utils.buildings.models import BuildingPaginationModel
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
    async def _get_count(self, *, session: AsyncSession) -> int:
        query = select(func.count()).select_from(
            select(BuildingDb).scalar_subquery()
        )
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
