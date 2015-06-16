"""empty message

Revision ID: 2fdc01092388
Revises: 14d18b31edfd
Create Date: 2015-06-15 21:10:56.367607

"""

# revision identifiers, used by Alembic.
revision = '2fdc01092388'
down_revision = '14d18b31edfd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bearer_token', sa.Column('remote_address', sa.String(length=45), nullable=True))
    op.add_column('bearer_token', sa.Column('user_agent', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bearer_token', 'user_agent')
    op.drop_column('bearer_token', 'remote_address')
    ### end Alembic commands ###