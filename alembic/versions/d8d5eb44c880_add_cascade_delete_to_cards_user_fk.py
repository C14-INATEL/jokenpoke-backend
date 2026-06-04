"""add_cascade_delete_to_cards_user_fk

Revision ID: d8d5eb44c880
Revises: 9ed4e933c720
Create Date: 2026-06-03 22:10:11.585829

"""

from collections.abc import Sequence

from alembic import op

revision: str = "d8d5eb44c880"
down_revision: str | Sequence[str] | None = "9ed4e933c720"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("cards_owner_id_fkey", "cards", type_="foreignkey")
    op.create_foreign_key(
        "cards_owner_id_fkey",
        "cards",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("cards_owner_id_fkey", "cards", type_="foreignkey")
    op.create_foreign_key("cards_owner_id_fkey", "cards", "users", ["owner_id"], ["id"])
