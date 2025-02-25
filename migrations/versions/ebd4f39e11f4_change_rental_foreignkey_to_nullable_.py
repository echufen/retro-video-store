"""change rental foreignkey to nullable true

Revision ID: ebd4f39e11f4
Revises: 2daa2099951a
Create Date: 2023-01-09 18:30:33.658956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebd4f39e11f4'
down_revision = '2daa2099951a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rental', 'customer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rental', 'video_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rental', 'video_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rental', 'customer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
