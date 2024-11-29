from uuid import UUID

from pydantic import BaseModel, root_validator, model_validator

from hot_wheels_collector.database.schemas import ModelCategory


# Toto zoskrejpujeme + series_name
class BaseHotWheelsModel(BaseModel):
    toy_no: str | None
    collection_no: str | None
    name: str
    category: ModelCategory = ModelCategory.car
    release_year: int | None
    color: str | None
    tampo: str | None
    base_color_type: str | None
    window_color: str | None
    interior_color: str | None
    wheel_type: str | None
    country: str | None
    description: str | None
    photo_url: str | None


class HotWheelsModelScraped(BaseHotWheelsModel):
    series_name: str | None
    # possibly release year :shruggy:


class HotWheelsModelResponse(BaseHotWheelsModel):
    id: UUID


class HotWheelsModelRequest(BaseHotWheelsModel):
    series_id: UUID


class GetSeriesRequest(BaseModel):
    series_name: str | None
    series_year: int | None

    @model_validator(mode="before")
    def at_least_one_field(cls, values):
        if not any(values):
            raise ValueError("series_request.at_least_one_field")

class GetSeriesResponse(BaseModel):
    id: UUID
    name: str
    release_year: int | None
    description: str | None
    # TODO: add models: list[HotWheelsModelResponse] = []
