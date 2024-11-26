import uuid

import pytest
from httpx import AsyncClient

from hot_wheels_collector.database.repository import HotWheelsRepository
from tests.mocks import SERIES_MOCK, MODEL_MOCK, GET_SERIES_MOCK


@pytest.mark.anyio
async def test_get_model(hw_repository: HotWheelsRepository, client: AsyncClient) -> None:
    res = await client.get(f"/model/{uuid.uuid4()}")
    assert res.status_code == 404

    series_id = await hw_repository.create_series(SERIES_MOCK)
    model_id = await hw_repository.create_model(MODEL_MOCK)
    res = await client.get(f"/model/{str(model_id)}")
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["toy_no"] == MODEL_MOCK.toy_no
    assert res_json["name"] == MODEL_MOCK.name
    assert res_json["series_id"] == str(series_id)
    assert res_json["description"] == MODEL_MOCK.description
    assert res_json["photo_url"] == str(MODEL_MOCK.photo_url)


@pytest.mark.anyio
async def test_get_series(hw_repository: HotWheelsRepository, client: AsyncClient) -> None:
    res = await client.get("/series", params={**GET_SERIES_MOCK.model_dump(exclude_none=True)})
    assert res.status_code == 404

    series_id = await hw_repository.create_series(SERIES_MOCK)
    res = await client.get("/series", params={**GET_SERIES_MOCK.model_dump(exclude_none=True), id: str(series_id)})
    assert res.status_code == 200
    assert res.json()["name"] == GET_SERIES_MOCK.name
