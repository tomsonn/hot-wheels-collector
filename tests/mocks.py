from pydantic import HttpUrl

from hot_wheels_collector.database.schemas import ModelCategory
from hot_wheels_collector.models.models import ScrapedHotWheelsModel
from hot_wheels_collector.models.series import CreateSeries, SeriesDetails

GET_SERIES_MOCK = SeriesDetails(
    name="Dummy Series",
)

SERIES_MOCK = CreateSeries(
    name="Dummy Series",
    release_year=6969,
    description="1 model series.",
)

MODEL_MOCK = ScrapedHotWheelsModel(
    name="Definitely a car",
    category=ModelCategory.car,
    toy_no="123G4",
    collection_no="collection_no",
    release_year=6969,
    color="red",
    tampo="wtf_is_this",
    base_color_type="blue",
    window_color="black",
    interior_color="black",
    wheel_type="69J",
    country="USA",
    description="The most expensive car in the world",
    photo_url=HttpUrl("https://definitely_a_photo_of_a_car.com"),
    series_name=SERIES_MOCK.name,
)
