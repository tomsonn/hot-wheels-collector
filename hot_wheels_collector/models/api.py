from uuid import UUID

from pydantic import BaseModel

from hot_wheels_collector.database.models import ModelCategory


class Model(BaseModel):
    id: int
    name: str
    category: ModelCategory
    release_year: int | None
    series_id: UUID | None
    description: str | None
