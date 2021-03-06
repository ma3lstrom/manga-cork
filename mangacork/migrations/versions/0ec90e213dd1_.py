"""empty message

Revision ID: 0ec90e213dd1
Revises: 33f541c958b4
Create Date: 2015-12-29 12:49:08.206267

"""

# revision identifiers, used by Alembic.
revision = '0ec90e213dd1'
down_revision = '33f541c958b4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=260), nullable=True),
    sa.Column('page', sa.String(length=80), nullable=True),
    sa.Column('chapter', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    ### end Alembic commands ###
