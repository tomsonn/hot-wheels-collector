from typing import Literal


from hot_wheels_collector.models.base import BaseHashableModel


class HWModel(BaseHashableModel):
    name: str
    collection_no: str | None = None
    color: str | None = None
    tampo: str | None = None
    base_color: str | None = None
    base_type: str | None = None
    window_color: str | None = None
    interior_color: str | None = None
    wheel_type: str | None = None
    toy_no: str | None = None
    cast_no: str | None = None
    toy_card: str | None = None
    scale: (
        Literal[
            "1:12",
            "1:125",
            "1:18",
            "1:20",
            "1:24",
            "1:32",
            "1:43",
            "1:50",
            "1:64",
            "1:87",
        ]
        | None
    ) = None
    country: str | None = None
    notes: str | None = None
    base_codes: str | None = None
    sequence_no: int | None = None
    release_year: int | None = None
    image_url: str | None = None
    case_no: str | None = None
    assortment_no: str | None = None
    release_after: bool | None = None
    TH: bool | None = None
    STH: bool | None = None
    mainline: bool | None = None
    card_variant: bool | None = None
    oversized_card: bool | None = None
