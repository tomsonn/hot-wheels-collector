import pytest
from sqlalchemy.exc import NoResultFound

from hot_wheels_collector.database.repository import HotWheelsRepository
from hot_wheels_collector.errors import SeriesAlreadyExistsError
from hot_wheels_collector.models.series import SeriesDetails
from tests.mocks import MODEL_MOCK, SERIES_MOCK


@pytest.mark.anyio
async def test_create_model(hw_repository: HotWheelsRepository) -> None:
    _ = await hw_repository.create_series(SERIES_MOCK)
    model_id = await hw_repository.create_model(MODEL_MOCK)
    assert model_id


@pytest.mark.anyio
async def test_create_model_series_not_exists(hw_repository: HotWheelsRepository) -> None:
    with pytest.raises(NoResultFound):
        await hw_repository.create_model(MODEL_MOCK)


@pytest.mark.anyio
async def test_create_series(hw_repository: HotWheelsRepository) -> None:
    series_id = await hw_repository.create_series(SERIES_MOCK)
    assert series_id

    series_db = await hw_repository.get_series(SeriesDetails(
        id=series_id
    ))
    assert series_db
    assert series_db.id == series_id
    assert series_db.name == SERIES_MOCK.name
    assert series_db.release_year == SERIES_MOCK.release_year
    assert series_db.description == SERIES_MOCK.description


@pytest.mark.anyio
async def test_create_series_already_exists(hw_repository: HotWheelsRepository) -> None:
    series_id = await hw_repository.create_series(SERIES_MOCK)
    assert series_id

    with pytest.raises(SeriesAlreadyExistsError):
        await hw_repository.create_series(SERIES_MOCK)
