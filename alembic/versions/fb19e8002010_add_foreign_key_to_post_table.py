"""add foreign-key to post table

Revision ID: fb19e8002010
Revises: bff9d16fcddd
Create Date: 2022-03-06 12:45:57.509214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb19e8002010'
down_revision = 'bff9d16fcddd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')

    pass
