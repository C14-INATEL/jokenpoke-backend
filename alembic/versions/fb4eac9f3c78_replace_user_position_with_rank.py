"""replace user position with rank

Revision ID: fb4eac9f3c78
Revises: 55f2ba512198
Create Date: 2026-06-02 19:48:41.032503

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fb4eac9f3c78"
down_revision: str | Sequence[str] | None = "55f2ba512198"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("rank", sa.String(), nullable=False, server_default="Beginner"),
    )
    op.drop_column("users", "position")
    op.alter_column("users", "rank", server_default=None)


def downgrade() -> None:
    op.add_column("users", sa.Column("position", sa.Integer(), nullable=True))
    op.drop_column("users", "rank")
