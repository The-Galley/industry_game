"""Init migration

Revision ID: 0a4210a6ae9e
Revises:
Create Date: 2024-02-24 23:47:10.452217

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0a4210a6ae9e"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_type = postgresql.ENUM("ADMIN", "PLAYER", name="user_type")
game_status = postgresql.ENUM(
    "CREATED", "STARTED", "PAUSED", "FINISHED", name="game_statuses"
)


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", user_type, nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.Column(
            "properties", postgresql.JSONB(), nullable=False, default="{}"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
    )
    op.create_index(
        op.f("ix__user__username"), "user", ["username"], unique=True
    )
    op.create_table(
        "game",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            game_status,
            server_default="CREATED",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
            name=op.f("fk__game__created_by_id__user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__game")),
    )
    op.create_index(
        op.f("ix__game__created_by_id"),
        "game",
        ["created_by_id"],
        unique=False,
    )
    op.create_table(
        "user_game_lobby",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["game.id"],
            name=op.f("fk__user_game_lobby__game_id__game"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk__user_game_lobby__user_id__user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "game_id", name=op.f("pk__user_game_lobby")
        ),
    )


def downgrade() -> None:
    op.drop_table("user_game_lobby")
    op.drop_index(op.f("ix__game__created_by_id"), table_name="game")
    op.drop_table("game")
    op.drop_index(op.f("ix__user__username"), table_name="user")
    op.drop_table("user")
    bind = op.get_bind()
    user_type.drop(bind)
    game_status.drop(bind)
