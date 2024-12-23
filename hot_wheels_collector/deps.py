from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.engine import Database
from hot_wheels_collector.database.repository import HotWheelsRepository
from hot_wheels_collector.settings.base import Settings
from hot_wheels_collector.settings.logger import configure_logger


class DependencyRegistry:
    settings: Settings = Settings()  # type: ignore
    logger: BoundLogger = configure_logger()
    db: Database = Database(settings)
    hw_repository: HotWheelsRepository = HotWheelsRepository(db, logger)


def create_deps() -> DependencyRegistry:
    return DependencyRegistry()
