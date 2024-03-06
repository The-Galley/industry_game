import asyncio

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Game as GameDb
from industry_game.db.models import GameStatus
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.games.models import Game, GamePaginationResponse
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
        page: int,
        page_size: int,
        status: GameStatus | None = None,
    ) -> GamePaginationResponse:
        total, items = await asyncio.gather(
            self.count(status=status),
            self.get_items(page=page, page_size=page_size, status=status),
        )
        return GamePaginationResponse(
            meta=MetaPagination.create(
                total=total,
                page=page,
                page_size=page_size,
            ),
            items=items,
        )

    @inject_session
    async def count(
        self,
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
        session: AsyncSession,
        page: int,
        page_size: int,
        status: GameStatus | None = None,
    ) -> list[Game]:
        query = select(GameDb).limit(page_size).offset((page - 1) * page_size)
        if status is not None:
            query = query.where(GameDb.status == status)
        games = await session.scalars(query.order_by(GameDb.name))
        items: list[Game] = []
        for game in games:
            items.append(Game.from_model(game))
        return items

    @inject_session
    async def create(
        self,
        session: AsyncSession,
        name: str,
        description: str,
        created_by_id: int,
        commit: bool = True,
    ) -> Game:
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
        return Game.from_model(game)

    @inject_session
    async def update_text(
        self,
        session: AsyncSession,
        game_id: int,
        name: str | None,
        description: str | None,
        commit: bool = True,
    ) -> Game:
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
        game = (await session.scalars(stmt)).one()
        if commit:
            await session.commit()
        return Game.from_model(game)

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
