from datetime import datetime, UTC
from enum import Enum
from uuid import uuid4, UUID

from pydantic import HttpUrl
from sqlmodel import SQLModel, Field


class ModelCategory(str, Enum):
    car = "car"
    truck = "truck"
    motorcycle = "motorcycle"
    plane = "plane"
    boat = "boat"


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class ModelCondition(str, Enum):
    new = "new"
    unpacked = "unpacked"
    slightly_damaged = "slightly_damaged"
    damaged = "damaged"


class Series(SQLModel, table=True):
    __tablename__ = "series"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    release_year: int | None
    description: str | None


class Models(SQLModel, table=True):
    __tablename__ = "models"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    toy_no: str | None = Field(default=None, index=True)
    collection_no: str | None
    name: str = Field(index=True)
    category: ModelCategory = Field(default=ModelCategory.car)
    release_year: int | None = Field(index=True)
    series_id: UUID = Field(foreign_key="series.id")
    color: str | None = Field(index=True)
    tampo: str | None = Field(index=True)
    base_color_type: str | None
    window_color: str | None
    interior_color: str | None
    wheel_type: str | None
    country: str | None
    description: str | None
    photo_url: str | None


class UserModels(SQLModel, table=True):
    __tablename__ = "user_models"

    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    model_id: UUID = Field(foreign_key="models.id", index=True)
    notes: str | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))
    condition: ModelCondition = Field(default=ModelCondition.new, index=True)
    for_sale: bool
    for_change: bool
    price: float | None



class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default=uuid4, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    is_active: bool
    role: UserRole = Field(default=UserRole.user)
