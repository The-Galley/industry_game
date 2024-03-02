import asyncio
from collections.abc import Mapping

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import User as UserDb
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.base import UserType
from industry_game.utils.users.models import FullUser, ShortUser, UserPagination


class PlayerStorage(AbstractStorage):
    @inject_session
    async def create(
        self,
        session: AsyncSession,
        *,
        username: str,
        password_hash: str,
        properties: Mapping[str, str],
        commit: bool = True,
    ) -> FullUser:
        stmt = (
            insert(UserDb)
            .values(
                username=username,
                password_hash=password_hash,
                properties=properties,
            )
            .returning(UserDb)
        )
        obj = (await session.scalars(stmt)).one()
        if commit:
            await session.commit()
        return FullUser.from_model(obj)

    @inject_session
    async def read_by_id(
        self, session: AsyncSession, user_id: int
    ) -> FullUser | None:
        stmt = select(UserDb).where(
            UserDb.type == UserType.PLAYER,
            UserDb.id == user_id,
        )
        obj = (await session.scalars(stmt)).first()
        return FullUser.from_model(obj) if obj else None

    @inject_session
    async def read_by_username(
        self,
        session: AsyncSession,
        username: str,
    ) -> FullUser | None:
        stmt = select(UserDb).where(UserDb.username == username)
        obj = (await session.scalars(stmt)).first()
        return FullUser.from_model(obj) if obj else None

    @inject_session
    async def get_by_username_and_password_hash(
        self,
        session: AsyncSession,
        username: str,
        password_hash: str,
    ) -> FullUser | None:
        stmt = select(UserDb).where(
            UserDb.username == username,
            UserDb.password_hash == password_hash,
        )
        obj = (await session.scalars(stmt)).first()
        return FullUser.from_model(obj) if obj else None

    async def pagination(self, page: int, page_size: int) -> UserPagination:
        total, items = await asyncio.gather(
            self.count(), self.get_items(page=page, page_size=page_size)
        )
        return UserPagination(
            meta=MetaPagination.create(
                total=total,
                page=page,
                page_size=page_size,
            ),
            items=items,
        )

    @inject_session
    async def count(self, session: AsyncSession) -> int:
        query = select(func.count()).select_from(
            select(UserDb)
            .where(UserDb.type == UserType.PLAYER)
            .scalar_subquery()
        )
        return (await session.execute(query)).scalar_one()

    @inject_session
    async def get_items(
        self, session: AsyncSession, page: int, page_size: int
    ) -> list[ShortUser]:
        query = (
            select(UserDb)
            .where(UserDb.type == UserType.PLAYER)
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        players = await session.scalars(query)
        items: list[ShortUser] = []
        for player in players:
            items.append(ShortUser.from_model(player))
        return items
