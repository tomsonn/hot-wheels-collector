from hot_wheels_collector.models.models import HWModel
from hot_wheels_collector.models.series import HWSeries


SERIES_MOCK = HWSeries(
    category="Mainline",
    name="Dummy Series",
    release_year=6969,
    description="1 model series.",
)

MODEL_MOCK = HWModel(
    name="Definitely a car",
    toy_no="123G4",
    collection_no="collection_no",
    release_year=6969,
    color="red",
    tampo="wtf_is_this",
    base_color="blue",
    window_color="black",
    interior_color="black",
    wheel_type="69J",
    country="USA",
    notes="The most expensive car in the world",
    image_url="https://definitely_a_photo_of_a_car.com",
)
