from hot_wheels_collector.models.base import BaseHashableModel


class SeriesBase(BaseHashableModel):
    category: str
    name: str | None = None
    release_year: int | None = None


class HWSeries(BaseHashableModel):
    category: str
    name: str | None = None
    release_year: int | None = None
    description: str | None = None
