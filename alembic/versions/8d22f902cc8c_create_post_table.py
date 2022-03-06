"""create post table

Revision ID: 8d22f902cc8c
Revises: 
Create Date: 2022-03-06 11:51:01.057930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d22f902cc8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
