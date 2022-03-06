"""add content column to post table

Revision ID: 55c9517797e8
Revises: 8d22f902cc8c
Create Date: 2022-03-06 12:13:56.967763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55c9517797e8'
down_revision = '8d22f902cc8c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
