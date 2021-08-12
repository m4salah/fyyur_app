"""empty message

Revision ID: 03358f3dab0f
Revises: b37966c34573
Create Date: 2021-07-04 23:12:41.233385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03358f3dab0f'
down_revision = 'b37966c34573'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cities_city_key', 'cities', type_='unique')
    op.drop_constraint('cities_state_key', 'cities', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('cities_state_key', 'cities', ['state'])
    op.create_unique_constraint('cities_city_key', 'cities', ['city'])
    # ### end Alembic commands ###