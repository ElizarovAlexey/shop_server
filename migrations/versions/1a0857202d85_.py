"""empty message

Revision ID: 1a0857202d85
Revises: c2d716bdfb82
Create Date: 2021-09-06 12:33:52.630598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a0857202d85'
down_revision = 'c2d716bdfb82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cart', 'users', ['user_id'], ['id'])
    op.drop_constraint('products_cart_id_fkey', 'products', type_='foreignkey')
    op.drop_column('products', 'cart_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('cart_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('products_cart_id_fkey', 'products', 'cart', ['cart_id'], ['id'])
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'user_id')
    # ### end Alembic commands ###
