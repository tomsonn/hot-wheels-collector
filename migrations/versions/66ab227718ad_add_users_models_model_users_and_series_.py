"""add users, models, model_users and series tables

Revision ID: 66ab227718ad
Revises: 
Create Date: 2024-12-23 17:36:44.271604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '66ab227718ad'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('series',
    sa.Column('id', sqlmodel.AutoString(length=64), nullable=False),
    sa.Column('category', sqlmodel.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.AutoString(), nullable=True),
    sa.Column('release_year', sa.Integer(), nullable=True),
    sa.Column('description', sqlmodel.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_series_category'), 'series', ['category'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('username', sqlmodel.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.AutoString(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'user', name='userrole'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('models',
    sa.Column('id', sqlmodel.AutoString(length=64), nullable=False),
    sa.Column('collection_no', sqlmodel.AutoString(), nullable=True),
    sa.Column('name', sqlmodel.AutoString(), nullable=False),
    sa.Column('color', sqlmodel.AutoString(), nullable=True),
    sa.Column('tampo', sqlmodel.AutoString(), nullable=True),
    sa.Column('base_color', sqlmodel.AutoString(), nullable=True),
    sa.Column('base_type', sqlmodel.AutoString(), nullable=True),
    sa.Column('window_color', sqlmodel.AutoString(), nullable=True),
    sa.Column('interior_color', sqlmodel.AutoString(), nullable=True),
    sa.Column('wheel_type', sqlmodel.AutoString(), nullable=True),
    sa.Column('toy_no', sqlmodel.AutoString(), nullable=True),
    sa.Column('cast_no', sqlmodel.AutoString(), nullable=True),
    sa.Column('toy_card', sqlmodel.AutoString(), nullable=True),
    sa.Column('scale', sqlmodel.AutoString(), nullable=True),
    sa.Column('country', sqlmodel.AutoString(), nullable=True),
    sa.Column('notes', sqlmodel.AutoString(), nullable=True),
    sa.Column('base_codes', sqlmodel.AutoString(), nullable=True),
    sa.Column('series_id', sqlmodel.AutoString(), nullable=False),
    sa.Column('series_no', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('image_url', sqlmodel.AutoString(), nullable=True),
    sa.Column('case_no', sqlmodel.AutoString(), nullable=True),
    sa.Column('assortment_no', sqlmodel.AutoString(), nullable=True),
    sa.Column('release_after', sa.Boolean(), nullable=True),
    sa.Column('TH', sa.Boolean(), nullable=True),
    sa.Column('STH', sa.Boolean(), nullable=True),
    sa.Column('mainline', sa.Boolean(), nullable=True),
    sa.Column('card_variant', sa.Boolean(), nullable=True),
    sa.Column('oversized_card', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_models_name'), 'models', ['name'], unique=False)
    op.create_index(op.f('ix_models_toy_no'), 'models', ['toy_no'], unique=False)
    op.create_table('user_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('model_id', sqlmodel.AutoString(), nullable=False),
    sa.Column('notes', sqlmodel.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('condition', sa.Enum('new', 'unpacked', 'slightly_damaged', 'damaged', name='modelcondition'), nullable=False),
    sa.Column('for_sale', sa.Boolean(), nullable=False),
    sa.Column('for_change', sa.Boolean(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_models_condition'), 'user_models', ['condition'], unique=False)
    op.create_index(op.f('ix_user_models_model_id'), 'user_models', ['model_id'], unique=False)
    op.create_index(op.f('ix_user_models_user_id'), 'user_models', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_models_user_id'), table_name='user_models')
    op.drop_index(op.f('ix_user_models_model_id'), table_name='user_models')
    op.drop_index(op.f('ix_user_models_condition'), table_name='user_models')
    op.drop_table('user_models')
    op.drop_index(op.f('ix_models_toy_no'), table_name='models')
    op.drop_index(op.f('ix_models_name'), table_name='models')
    op.drop_table('models')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_series_category'), table_name='series')
    op.drop_table('series')
    # ### end Alembic commands ###