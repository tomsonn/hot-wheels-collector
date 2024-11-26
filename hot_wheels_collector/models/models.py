from uuid import UUID

from pydantic import BaseModel, HttpUrl

from hot_wheels_collector.database.schemas import ModelCategory
from hot_wheels_collector.models.series import SeriesDetails


class HotWheelsModel(BaseModel):
    name: str
    category: ModelCategory = ModelCategory.car
    toy_no: str | None = None
    collection_no: str | None = None
    release_year: int | None = None
    color: str | None = None
    tampo: str | None = None
    base_color_type: str | None = None
    window_color: str | None = None
    interior_color: str | None = None
    wheel_type: str | None = None
    country: str | None = None
    description: str | None = None
    photo_url: HttpUrl | None = None


class CreateHotWheelsModel(HotWheelsModel):
    series_id: UUID
    series_details: SeriesDetails


class ScrapedHotWheelsModel(HotWheelsModel):
    series_name: str


class HotWheelsModelResponse(HotWheelsModel):
    id: UUID
    series_id: UUID
