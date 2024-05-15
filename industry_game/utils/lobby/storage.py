import asyncio
from collections.abc import Sequence

from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import User as UserDb
from industry_game.db.models import UserGameLobby as UserGameLobbyDb
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.lobby.models import LobbyModel, LobbyPaginationModel
from industry_game.utils.pagination import MetaPagination


class LobbyStorage(AbstractStorage):
    async def pagination(
        self,
        game_id: int,
        limit: int,
        offset: int,
    ) -> LobbyPaginationModel:
        total, items = await asyncio.gather(
            self.count(),
            self.get_items(game_id=game_id, limit=limit, offset=offset),
        )
        return LobbyPaginationModel(
            meta=MetaPagination(total=total),
            items=items,
        )

    @inject_session
    async def read_by_id(
        self,
        session: AsyncSession,
        *,
        game_id: int,
        user_id: int,
    ) -> LobbyModel | None:
        obj = await session.get(
            UserGameLobbyDb,
            ident={"game_id": game_id, "user_id": user_id},
        )
        return LobbyModel.model_validate(obj) if obj else None

    @inject_session
    async def add_user(
        self,
        session: AsyncSession,
        game_id: int,
        user_id: int,
        commit: bool = True,
    ) -> None:
        query = insert(UserGameLobbyDb).values(
            game_id=game_id,
            user_id=user_id,
        )
        await session.execute(query)
        if commit:
            await session.commit()

    @inject_session
    async def delete(
        self,
        session: AsyncSession,
        game_id: int,
        user_id: int,
        commit: bool = True,
    ) -> None:
        stmt = delete(UserGameLobbyDb).where(
            UserGameLobbyDb.game_id == game_id,
            UserGameLobbyDb.user_id == user_id,
        )
        await session.execute(stmt)
        if commit:
            await session.commit()

    @inject_session
    async def count(self, *, session: AsyncSession) -> int:
        query = select(func.count()).select_from(UserGameLobbyDb)
        return (await session.execute(query)).scalar_one()

    @inject_session
    async def get_items(
        self,
        *,
        session: AsyncSession,
        game_id: int,
        limit: int,
        offset: int,
    ) -> Sequence[UserDb]:
        query = (
            select(UserDb)
            .join(UserGameLobbyDb, UserDb.id == UserGameLobbyDb.user_id)
            .where(UserGameLobbyDb.game_id == game_id)
            .limit(limit)
            .offset(offset)
        )
        return (await session.scalars(query)).all()
