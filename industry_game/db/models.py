from collections.abc import Mapping
from enum import StrEnum, unique
from typing import Any

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from industry_game.db.base import Base, StartFinishMixin, TimestampMixin
from industry_game.utils.db import make_pg_enum
from industry_game.utils.users.base import UserType


@unique
class GameStatus(StrEnum):
    CREATED = "CREATED"
    STARTED = "STARTED"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"


@unique
class BuildingStatuses(StrEnum):
    CONSTRUCTION = "CONSTRUCTION"  # строится
    BUILT = "BUILT"  # построено
    PROCESSING = "PROCESSING"  # вырабатывает ресурс


@unique
class Resources(StrEnum):  # ресурсы
    METALL = "METALL"
    CHEMICAL = "CHEMICAL"
    MACHINE = "MACHINE"
    LIGHT_INDUSTRY = "LIGHT_INDUSTRY"
    FOOD_INDUSTRY = "FOOD_INDUSTRY"
    PEOPLE = "PEOPLE"
    EDUCATED_PEOPLE = "EDUCATED_PEOPLE"
    BITCOIN = "BITCOIN"


@unique
class Sector(StrEnum):  # отрасль производства
    INDUSTRY = "INDUSTRY"
    PEOPLE = "PEOPLE"
    LOGISTIC = "LOGISTIC"


@unique
class Level(StrEnum):
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"


@unique
class DistrictRoles(StrEnum):
    pass


class User(Base, TimestampMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[UserType] = mapped_column(
        make_pg_enum(UserType, name="user_type"),
        nullable=False,
        default=UserType.PLAYER.value,
    )
    username: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
        unique=True,
    )
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    properties: Mapped[Mapping[str, Any]] = mapped_column(
        JSONB(),
        nullable=False,
        default="{}",
    )


class Game(Base, TimestampMixin, StartFinishMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        default="",
    )
    created_by_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[GameStatus] = mapped_column(
        make_pg_enum(GameStatus, name="game_statuses"),
        nullable=False,
        server_default=GameStatus.CREATED.value,
    )

    created_by: Mapped[User] = relationship("User")


class UserGameLobby(Base):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("game.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    user: Mapped[User] = relationship(User)
    game: Mapped[Game] = relationship(Game)
