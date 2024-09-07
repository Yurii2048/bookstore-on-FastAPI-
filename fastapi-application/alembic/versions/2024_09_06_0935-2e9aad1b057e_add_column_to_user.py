"""add column to user

Revision ID: 2e9aad1b057e
Revises: 411d8bd864a0
Create Date: 2024-09-06 09:35:45.751269

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e9aad1b057e"
down_revision: Union[str, None] = "411d8bd864a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("password", sa.String(), nullable=False))
    op.add_column("users", sa.Column("email", sa.String(), nullable=True))
    op.add_column("users", sa.Column("active", sa.Boolean(), nullable=False))
    op.drop_column("users", "hashed_password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "hashed_password",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("users", "active")
    op.drop_column("users", "email")
    op.drop_column("users", "password")
    # ### end Alembic commands ###
