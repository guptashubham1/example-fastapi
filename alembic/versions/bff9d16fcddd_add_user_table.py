"""add user table

Revision ID: bff9d16fcddd
Revises: 55c9517797e8
Create Date: 2022-03-06 12:28:18.693367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff9d16fcddd'
down_revision = '55c9517797e8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False)),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    pass


def downgrade():
    op.drop_table('users')
    pass
