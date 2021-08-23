"""empty message

Revision ID: 06d573192bb8
Revises: 4b02051cfacf
Create Date: 2021-08-20 14:35:32.395705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06d573192bb8'
down_revision = '4b02051cfacf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_title', sa.String(length=120), nullable=False),
    sa.Column('product_price', sa.Integer(), nullable=False),
    sa.Column('product_image', sa.String(length=120), nullable=False),
    sa.Column('product_size', sa.Integer(), nullable=False),
    sa.Column('product_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    # ### end Alembic commands ###
