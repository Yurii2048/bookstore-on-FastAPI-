"""create book table

Revision ID: 0b610d0d40ec
Revises: 19983bd7959d
Create Date: 2024-08-29 20:26:36.211234

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0b610d0d40ec"
down_revision: Union[str, None] = "19983bd7959d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("prise", sa.Integer(), nullable=False),

        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )


def downgrade() -> None:

    op.drop_table("books")
