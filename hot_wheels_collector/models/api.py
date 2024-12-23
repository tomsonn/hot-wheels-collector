from pydantic import BaseModel

from hot_wheels_collector.models.series import HWSeries


class FilteredSeriesResponse(BaseModel):
    series: list[HWSeries]
