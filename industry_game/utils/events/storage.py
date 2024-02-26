from collections.abc import Mapping
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from industry_game.db.models import Event
from industry_game.utils.db import AbstractStorage, inject_session
from industry_game.utils.events.base import EventStatus, EventType


class EventStorage(AbstractStorage):
    @inject_session
    async def create(
        self,
        session: AsyncSession,
        game_id: int,
        status: EventStatus,
        type: EventType,
        created_at: datetime,
        started_at: datetime | None,
        ended_at: datetime | None,
        during_sec: int,
        properties: Mapping[str, Any],
        *,
        commit: bool = True,
    ) -> Event:
        stmt = (
            insert(Event)
            .values(
                game_id=game_id,
                status=status,
                type=type,
                created_at=created_at,
                started_at=started_at,
                ended_at=ended_at,
                during_sec=during_sec,
                properties=properties,
            )
            .returning(Event)
        )
        result = await session.scalars(stmt)
        if commit:
            await session.commit()
        return result.one()

    @inject_session
    async def update_status(
        self,
        session: AsyncSession,
        event_uuid: UUID,
        status: EventStatus,
        *,
        commit: bool = True,
    ) -> None:
        stmt = (
            update(Event).where(Event.uuid == event_uuid).values(status=status)
        )
        await session.execute(stmt)
        if commit:
            await session.commit()
