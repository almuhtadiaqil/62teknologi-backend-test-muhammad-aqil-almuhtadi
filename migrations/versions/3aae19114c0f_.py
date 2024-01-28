"""empty message

Revision ID: 3aae19114c0f
Revises: 
Create Date: 2024-01-27 20:44:56.992767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aae19114c0f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('alias', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('is_closed', sa.Boolean(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('review_count', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Double(), nullable=True),
    sa.Column('longitude', sa.Double(), nullable=True),
    sa.Column('transactions', sa.Text(), nullable=True),
    sa.Column('price', sa.String(length=255), nullable=True),
    sa.Column('address1', sa.String(length=255), nullable=True),
    sa.Column('address2', sa.String(length=255), nullable=True),
    sa.Column('address3', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('zip_code', sa.String(length=6), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('state', sa.String(length=10), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('display_phone', sa.String(length=20), nullable=True),
    sa.Column('distance', sa.Double(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=225), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('business')
    # ### end Alembic commands ###