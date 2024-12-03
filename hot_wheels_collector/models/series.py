from uuid import UUID

from pydantic import BaseModel, model_validator

from hot_wheels_collector.errors import GetSeriesQueryError


class SeriesDetails(BaseModel):
    name: str | None = None
    id: UUID | None = None
    release_year: int | None = None

    @model_validator(mode="after")
    def name_or_id(cls, values):
        if not any([values.name, values.id]):
            raise GetSeriesQueryError("series_request.name_or_id")
        return values


class GetSeriesResponse(BaseModel):
    id: UUID
    name: str
    release_year: int | None = None
    description: str | None = None
    # TODO: add models: list[HotWheelsModelResponse] = []


class CreateSeries(BaseModel):
    name: str
    release_year: int | None = None
    description: str | None = None
