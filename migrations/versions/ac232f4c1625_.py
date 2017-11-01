"""empty message

Revision ID: ac232f4c1625
Revises: bd314a1a5e69
Create Date: 2017-11-01 11:29:44.828414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac232f4c1625'
down_revision = 'bd314a1a5e69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enquiries', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('enquiries_user_fkey', 'enquiries', type_='foreignkey')
    op.create_foreign_key(None, 'enquiries', 'users', ['user_id'], ['id'])
    op.drop_column('enquiries', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enquiries', sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'enquiries', type_='foreignkey')
    op.create_foreign_key('enquiries_user_fkey', 'enquiries', 'users', ['user'], ['id'])
    op.drop_column('enquiries', 'user_id')
    # ### end Alembic commands ###
