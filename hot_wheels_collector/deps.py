from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.engine import Database, get_db
from hot_wheels_collector.database.repository import HotWheelsRepository, get_repository
from hot_wheels_collector.settings.base import Settings, get_settings
from hot_wheels_collector.settings.logger import get_logger


class DependencyRegistry:
    settings: Settings = get_settings()  # type: ignore
    logger: BoundLogger = get_logger()
    db: Database = get_db()
    hw_repository: HotWheelsRepository = get_repository(db, logger)


def create_deps() -> DependencyRegistry:
    return DependencyRegistry()
