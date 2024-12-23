from datetime import datetime, UTC
from enum import Enum
from uuid import uuid4, UUID

from sqlmodel import SQLModel, Field


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class ModelCondition(str, Enum):
    new = "new"
    unpacked = "unpacked"
    slightly_damaged = "slightly_damaged"
    damaged = "damaged"


class Series(SQLModel, table=True):
    __tablename__: str = "series"  # type: ignore

    id: str = Field(primary_key=True, max_length=64)
    category: str = Field(index=True)
    name: str | None
    release_year: int | None
    description: str | None


class Models(SQLModel, table=True):
    __tablename__: str = "models"  # type: ignore

    id: str = Field(primary_key=True, max_length=64)
    collection_no: str | None
    name: str = Field(index=True)
    color: str | None
    tampo: str | None
    base_color: str | None
    base_type: str | None
    window_color: str | None
    interior_color: str | None
    wheel_type: str | None
    toy_no: str | None = Field(index=True)
    cast_no: str | None
    toy_card: str | None
    scale: str | None
    country: str | None
    notes: str | None
    base_codes: str | None
    series_id: str = Field(foreign_key="series.id")
    series_no: int | None
    year: int | None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    image_url: str | None
    case_no: str | None
    assortment_no: str | None
    release_after: bool | None
    TH: bool | None
    STH: bool | None
    mainline: bool | None
    card_variant: bool | None
    oversized_card: bool | None


class UserModels(SQLModel, table=True):
    __tablename__: str = "user_models"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    model_id: str = Field(foreign_key="models.id", index=True)
    notes: str | None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    condition: ModelCondition = Field(default=ModelCondition.new, index=True)
    for_sale: bool
    for_change: bool
    price: float | None


class User(SQLModel, table=True):
    __tablename__: str = "users"  # type: ignore

    id: UUID = Field(default=uuid4, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    is_active: bool
    role: UserRole = Field(default=UserRole.user)
