"""add table check

Revision ID: 6b4c3f4d053e
Revises: 8e529df69087
Create Date: 2020-07-14 19:16:00.776685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b4c3f4d053e'
down_revision = '8e529df69087'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('check_product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('int_product', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('check_product')
    # ### end Alembic commands ###
