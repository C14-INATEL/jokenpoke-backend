"""Add ranking columns to users

Revision ID: 55f2ba512198
Revises: ce687966a963
Create Date: 2026-05-25 19:21:04.491386

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "55f2ba512198"
down_revision: str | Sequence[str] | None = "ce687966a963"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # server_default="0" necessário para NOT NULL em tabelas com dados existentes
    op.add_column(
        "users", sa.Column("points", sa.Integer(), nullable=False, server_default="0")
    )
    op.add_column("users", sa.Column("position", sa.Integer(), nullable=True))
    # Remove o server_default após popular as linhas existentes
    op.alter_column("users", "points", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "position")
    op.drop_column("users", "points")
