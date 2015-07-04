"""empty message

Revision ID: dac0423c0e3
Revises: 14566cb3ec6d
Create Date: 2015-07-04 13:17:38.382982

"""

# revision identifiers, used by Alembic.
revision = 'dac0423c0e3'
down_revision = '14566cb3ec6d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device_type', sa.Column('zway_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'device_type', ['zway_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'device_type', type_='unique')
    op.drop_column('device_type', 'zway_id')
    ### end Alembic commands ###