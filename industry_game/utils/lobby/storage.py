import asyncio

from sqlalchemy import delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import User as UserDb
from industry_game.db.models import UserGameLobby as UserGameLobbyDb
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.lobby.models import Lobby, LobbyPagination
from industry_game.utils.pagination import MetaPagination
from industry_game.utils.users.models import ShortUser


class LobbyStorage(AbstractStorage):
    async def pagination(
        self, game_id: int, page: int, page_size: int
    ) -> LobbyPagination:
        total, items = await asyncio.gather(
            self.count(),
            self.get_items(game_id=game_id, page=page, page_size=page_size),
        )
        return LobbyPagination(
            meta=MetaPagination.create(
                total=total,
                page=page,
                page_size=page_size,
            ),
            items=items,
        )

    @inject_session
    async def read_by_id(
        self,
        session: AsyncSession,
        *,
        game_id: int,
        user_id: int,
    ) -> Lobby | None:
        obj = await session.get(
            UserGameLobbyDb,
            ident={"game_id": game_id, "user_id": user_id},
        )
        return Lobby.from_model(obj) if obj else None

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
    async def count(self, session: AsyncSession) -> int:
        query = select(func.count()).select_from(UserGameLobbyDb)
        return (await session.execute(query)).scalar_one()

    @inject_session
    async def get_items(
        self, session: AsyncSession, game_id: int, page: int, page_size: int
    ) -> list[ShortUser]:
        query = (
            select(UserDb)
            .join(UserGameLobbyDb, UserDb.id == UserGameLobbyDb.user_id)
            .where(UserGameLobbyDb.game_id == game_id)
            .limit(page_size)
            .offset((page - 1) * page_size)
        )

        games = await session.scalars(query)
        items: list[ShortUser] = []
        for game in games:
            items.append(ShortUser.from_model(game))
        return items
