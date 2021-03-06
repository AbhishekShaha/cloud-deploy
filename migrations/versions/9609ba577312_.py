"""empty message

Revision ID: 9609ba577312
Revises: c7aab03f2932
Create Date: 2017-10-31 17:28:23.862574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9609ba577312'
down_revision = 'c7aab03f2932'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'rating')
    op.add_column('reviews', sa.Column('rating', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'rating')
    op.add_column('books', sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
