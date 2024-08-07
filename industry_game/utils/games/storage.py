import asyncio
from collections.abc import Sequence

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Game as GameDb
from industry_game.db.models import GameStatus
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.games.models import (
    Game,
    GameModel,
    GamePaginationModel,
)
from industry_game.utils.pagination import MetaPagination


class GameStorage(AbstractStorage):
    @inject_session
    async def get_by_id(
        self, session: AsyncSession, game_id: int
    ) -> Game | None:
        game = await session.get(GameDb, game_id)
        if game is None:
            return None
        return Game.from_model(game)

    async def pagination(
        self,
        limit: int,
        offset: int,
        status: GameStatus | None = None,
    ) -> GamePaginationModel:
        total, items = await asyncio.gather(
            self.count(status=status),
            self.get_items(status=status, limit=limit, offset=offset),
        )
        return GamePaginationModel(
            meta=MetaPagination(total=total),
            items=items,
        )

    @inject_session
    async def count(
        self,
        *,
        session: AsyncSession,
        status: GameStatus | None = None,
    ) -> int:
        query = select(GameDb)
        if status is not None:
            query = query.where(GameDb.status == status)
        stmt = select(func.count()).select_from(query.subquery())
        return (await session.execute(stmt)).scalar_one()

    @inject_session
    async def get_items(
        self,
        *,
        session: AsyncSession,
        limit: int,
        offset: int,
        status: GameStatus | None = None,
    ) -> Sequence[GameDb]:
        query = select(GameDb).limit(limit).offset(offset)
        if status is not None:
            query = query.where(GameDb.status == status)
        return (await session.scalars(query.order_by(GameDb.name))).all()

    @inject_session
    async def create(
        self,
        *,
        session: AsyncSession,
        name: str,
        description: str,
        created_by_id: int,
        commit: bool = True,
    ) -> GameModel:
        stmt = (
            insert(GameDb)
            .values(
                name=name,
                description=description,
                created_by_id=created_by_id,
            )
            .returning(GameDb)
        )
        game = (await session.scalars(stmt)).one()
        if commit:
            await session.commit()
        return GameModel.model_validate(game)

    @inject_session
    async def update_text(
        self,
        session: AsyncSession,
        game_id: int,
        name: str | None,
        description: str | None,
        commit: bool = True,
    ) -> Game | None:
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description

        stmt = (
            update(GameDb)
            .where(GameDb.id == game_id)
            .values(**data)
            .returning(GameDb)
        )
        game = (await session.scalars(stmt)).first()
        if commit:
            await session.commit()
        return Game.from_model(game) if game else None

    @inject_session
    async def update_status(
        self,
        session: AsyncSession,
        game_id: int,
        status: GameStatus,
        commit: bool = True,
    ) -> Game:
        stmt = (
            update(GameDb)
            .where(GameDb.id == game_id)
            .values(status=status)
            .returning(GameDb)
        )
        game = (await session.scalars(stmt)).one()
        if commit:
            await session.commit()
        return Game.from_model(game)
