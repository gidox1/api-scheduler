"""Cascade on delete

Revision ID: 398fa16eb17f
Revises: 4a07623cd83c
Create Date: 2023-06-30 15:31:17.908849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '398fa16eb17f'
down_revision = '4a07623cd83c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organization', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organization', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###