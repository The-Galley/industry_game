import asyncio

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Game as GameDb
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.games.models import Game, GamePagination
from industry_game.utils.pagination import MetaPagination


class GameStorage(AbstractStorage):
    @inject_session
    async def read_by_id(
        self, session: AsyncSession, game_id: int
    ) -> Game | None:
        game = await session.get(GameDb, game_id)
        if game is None:
            return None
        return Game.from_model(game)

    async def pagination(self, page: int, page_size: int) -> GamePagination:
        total, items = await asyncio.gather(
            self.count(),
            self.get_items(page=page, page_size=page_size),
        )
        return GamePagination(
            meta=MetaPagination.create(
                total=total,
                page=page,
                page_size=page_size,
            ),
            items=items,
        )

    @inject_session
    async def count(self, session: AsyncSession) -> int:
        query = select(func.count()).select_from(GameDb)
        return (await session.execute(query)).scalar_one()

    @inject_session
    async def get_items(
        self, session: AsyncSession, page: int, page_size: int
    ) -> list[Game]:
        query = select(GameDb).limit(page_size).offset((page - 1) * page_size)

        games = await session.scalars(query)
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
        created_by: int,
        commit: bool = True,
    ) -> Game:
        stmt = (
            insert(GameDb)
            .values(
                name=name,
                description=description,
                created_by=created_by,
            )
            .returning(GameDb)
        )
        game = (await session.scalars(stmt)).one()
        if commit:
            await session.commit()
        return Game.from_model(game)

    @inject_session
    async def update(
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
