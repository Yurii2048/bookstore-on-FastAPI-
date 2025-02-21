"""change the column type (password in user)

Revision ID: 9905d8b896bb
Revises: 2e9aad1b057e
Create Date: 2024-09-06 10:58:20.444690

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9905d8b896bb"
down_revision: Union[str, None] = "2e9aad1b057e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    # ### end Alembic commands ###
