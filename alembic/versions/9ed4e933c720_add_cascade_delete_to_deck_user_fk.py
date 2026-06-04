"""add_cascade_delete_to_deck_user_fk

Revision ID: 9ed4e933c720
Revises: fb4eac9f3c78
Create Date: 2026-06-03 21:54:31.114243

"""

from collections.abc import Sequence

from alembic import op

revision: str = "9ed4e933c720"
down_revision: str | Sequence[str] | None = "fb4eac9f3c78"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("deck_user_id_fkey", "deck", type_="foreignkey")
    op.create_foreign_key(
        "deck_user_id_fkey", "deck", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("deck_user_id_fkey", "deck", type_="foreignkey")
    op.create_foreign_key("deck_user_id_fkey", "deck", "users", ["user_id"], ["id"])
