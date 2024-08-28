"""create order table

Revision ID: c60b8b2ca2ec
Revises: 1ac012ba2b39
Create Date: 2024-08-28 11:00:38.301296

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c60b8b2ca2ec"
down_revision: Union[str, None] = "1ac012ba2b39"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("order_status", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_create", sa.DateTime(), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_orders_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )


def downgrade() -> None:
    op.drop_table("orders")
