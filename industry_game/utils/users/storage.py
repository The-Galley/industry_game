import asyncio
from collections.abc import Mapping, Sequence

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import User as UserDb
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.base import UserType
from industry_game.utils.users.models import User, UserPaginationModel


class UserStorage(AbstractStorage):
    @inject_session
    async def create(
        self,
        session: AsyncSession,
        *,
        username: str,
        password_hash: str,
        properties: Mapping[str, str],
        commit: bool = True,
    ) -> User:
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
        return User.from_model(obj)

    @inject_session
    async def read_by_id(
        self, session: AsyncSession, user_id: int
    ) -> User | None:
        stmt = select(UserDb).where(
            UserDb.type == UserType.PLAYER,
            UserDb.id == user_id,
        )
        obj = (await session.scalars(stmt)).first()
        return User.from_model(obj) if obj else None

    @inject_session
    async def read_by_username(
        self,
        session: AsyncSession,
        username: str,
    ) -> User | None:
        stmt = select(UserDb).where(UserDb.username == username)
        obj = (await session.scalars(stmt)).first()
        return User.from_model(obj) if obj else None

    @inject_session
    async def get_by_username_and_password_hash(
        self,
        session: AsyncSession,
        username: str,
        password_hash: str,
    ) -> User | None:
        stmt = select(UserDb).where(
            UserDb.username == username,
            UserDb.password_hash == password_hash,
        )
        obj = (await session.scalars(stmt)).first()
        return User.from_model(obj) if obj else None

    async def pagination(
        self, page: int, page_size: int
    ) -> UserPaginationModel:
        total, items = await asyncio.gather(
            self._get_count(user_type=UserType.PLAYER),
            self._get_items(
                user_type=UserType.PLAYER,
                page=page,
                page_size=page_size,
            ),
        )
        return UserPaginationModel(
            meta=MetaPagination.create(
                total=total,
                page=page,
                page_size=page_size,
            ),
            items=items,
        )

    @inject_session
    async def _get_count(
        self,
        session: AsyncSession,
        user_type: UserType,
    ) -> int:
        query = select(func.count()).select_from(
            select(UserDb).where(UserDb.type == user_type).scalar_subquery()
        )
        return (await session.execute(query)).scalar_one()

    @inject_session
    async def _get_items(
        self,
        session: AsyncSession,
        user_type: UserType,
        page: int,
        page_size: int,
    ) -> Sequence[User]:
        query = (
            select(UserDb)
            .where(UserDb.type == user_type)
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        players = await session.scalars(query)
        items: list[User] = []
        for player in players:
            items.append(User.from_model(player))
        return items
