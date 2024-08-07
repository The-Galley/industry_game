import re
from datetime import UTC, datetime

from sqlalchemy import DateTime, MetaData, text
from sqlalchemy.orm import (
    Mapped,
    as_declarative,
    declarative_mixin,
    declared_attr,
    mapped_column,
)

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

metadata = MetaData(naming_convention=convention)  # type:ignore[arg-type]


@as_declarative(metadata=metadata)
class Base:
    metadata: MetaData

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        return "_".join(name_list).lower()


@declarative_mixin
class TimestampMixin:
    @declared_attr
    @classmethod
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=text("timezone('utc', now())"),
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=text("timezone('utc', now())"),
            server_onupdate=text("timezone('utc', now())"),  # type:ignore[arg-type]
            onupdate=lambda: datetime.now(tz=UTC),
        )


@declarative_mixin
class StartFinishMixin:
    @declared_attr
    def started_at(cls) -> Mapped[datetime | None]:
        return mapped_column(DateTime(timezone=True), nullable=True)

    @declared_attr
    def finished_at(cls) -> Mapped[datetime | None]:
        return mapped_column(DateTime(timezone=True), nullable=True)
