"""add_cascade_delete_to_deck_card_fk

Revision ID: 7c48bc9f87c5
Revises: d8d5eb44c880
Create Date: 2026-06-04 16:44:56.520788

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c48bc9f87c5"
down_revision: str | Sequence[str] | None = "d8d5eb44c880"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("deck_card_id_fkey", "deck", type_="foreignkey")
    op.create_foreign_key(
        "deck_card_id_fkey", "deck", "cards", ["card_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("deck_card_id_fkey", "deck", type_="foreignkey")
    op.create_foreign_key("deck_card_id_fkey", "deck", "cards", ["card_id"], ["id"])
