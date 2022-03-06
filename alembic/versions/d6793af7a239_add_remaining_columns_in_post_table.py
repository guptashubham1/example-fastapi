"""add remaining columns in post table

Revision ID: d6793af7a239
Revises: fb19e8002010
Create Date: 2022-03-06 13:34:27.882331

"""
import time
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6793af7a239'
down_revision = 'fb19e8002010'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
