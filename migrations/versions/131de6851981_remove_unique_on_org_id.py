"""Remove unique on org_id

Revision ID: 131de6851981
Revises: 719c55132efc
Create Date: 2023-07-11 22:08:06.212945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '131de6851981'
down_revision = '719c55132efc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('franchise', schema=None) as batch_op:
        batch_op.drop_index('organization_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('franchise', schema=None) as batch_op:
        batch_op.create_index('organization_id', ['organization_id'], unique=False)

    # ### end Alembic commands ###
