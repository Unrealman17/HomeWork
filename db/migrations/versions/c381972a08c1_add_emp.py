"""add emp

Revision ID: c381972a08c1
Revises: 
Create Date: 2021-01-24 14:34:41.813520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c381972a08c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emp',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=20), nullable=False),
    sa.Column('pwd', sa.VARBINARY(), nullable=False),
    sa.Column('login', sa.VARCHAR(length=64), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('position', sa.VARCHAR(length=64), nullable=True),
    sa.Column('department', sa.VARCHAR(length=64), nullable=True),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('login')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('emp')
    # ### end Alembic commands ###
