"""add users, models, model_users and series tables

Revision ID: 443959e98cc6
Revises:
Create Date: 2024-11-27 20:45:22.114666

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "443959e98cc6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "series",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.AutoString(), nullable=False),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.Column("description", sqlmodel.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_series_name"), "series", ["name"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sqlmodel.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.AutoString(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("role", sa.Enum("admin", "user", name="userrole"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)
    op.create_table(
        "models",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("toy_no", sqlmodel.AutoString(), nullable=False),
        sa.Column("collection_no", sqlmodel.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.AutoString(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "car", "truck", "motorcycle", "plane", "boat", name="modelcategory"
            ),
            nullable=False,
        ),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.Column("series_id", sa.Uuid(), nullable=False),
        sa.Column("color", sqlmodel.AutoString(), nullable=True),
        sa.Column("tampo", sqlmodel.AutoString(), nullable=True),
        sa.Column("base_color_type", sqlmodel.AutoString(), nullable=True),
        sa.Column("window_color", sqlmodel.AutoString(), nullable=True),
        sa.Column("interior_color", sqlmodel.AutoString(), nullable=True),
        sa.Column("wheel_type", sqlmodel.AutoString(), nullable=True),
        sa.Column("country", sqlmodel.AutoString(), nullable=True),
        sa.Column("description", sqlmodel.AutoString(), nullable=True),
        sa.Column("photo_url", sqlmodel.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["series.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_models_color"), "models", ["color"], unique=False)
    op.create_index(op.f("ix_models_name"), "models", ["name"], unique=False)
    op.create_index(
        op.f("ix_models_release_year"), "models", ["release_year"], unique=False
    )
    op.create_index(op.f("ix_models_tampo"), "models", ["tampo"], unique=False)
    op.create_index(op.f("ix_models_toy_no"), "models", ["toy_no"], unique=False)
    op.create_table(
        "user_models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("model_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sqlmodel.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "condition",
            sa.Enum(
                "new", "unpacked", "slightly_damaged", "damaged", name="modelcondition"
            ),
            nullable=False,
        ),
        sa.Column("for_sale", sa.Boolean(), nullable=False),
        sa.Column("for_change", sa.Boolean(), nullable=False),
        sa.Column("price", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["model_id"],
            ["models.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_models_condition"), "user_models", ["condition"], unique=False
    )
    op.create_index(
        op.f("ix_user_models_model_id"), "user_models", ["model_id"], unique=False
    )
    op.create_index(
        op.f("ix_user_models_user_id"), "user_models", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_models_user_id"), table_name="user_models")
    op.drop_index(op.f("ix_user_models_model_id"), table_name="user_models")
    op.drop_index(op.f("ix_user_models_condition"), table_name="user_models")
    op.drop_table("user_models")
    op.drop_index(op.f("ix_models_toy_no"), table_name="models")
    op.drop_index(op.f("ix_models_tampo"), table_name="models")
    op.drop_index(op.f("ix_models_release_year"), table_name="models")
    op.drop_index(op.f("ix_models_name"), table_name="models")
    op.drop_index(op.f("ix_models_color"), table_name="models")
    op.drop_table("models")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_series_name"), table_name="series")
    op.drop_table("series")
    # ### end Alembic commands ###