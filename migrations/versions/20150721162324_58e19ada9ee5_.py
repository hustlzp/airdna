"""empty message

Revision ID: 58e19ada9ee5
Revises: 49086f55444e
Create Date: 2015-07-21 16:23:24.026509

"""

# revision identifiers, used by Alembic.
revision = '58e19ada9ee5'
down_revision = '49086f55444e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('introduction', sa.String(length=200), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'introduction')
    ### end Alembic commands ###
