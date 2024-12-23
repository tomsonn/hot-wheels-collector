import sys
import asyncio

from requests import HTTPError

from hot_wheels_collector.deps import create_deps
from hot_wheels_collector.scrapers.hot_wheels_models import HotWheelsModels


if __name__ == "__main__":
    dependencies = create_deps()
    logger = dependencies.logger

    try:
        logger.info("scraper.start")
        hot_wheels_scraper = HotWheelsModels(
            dependencies.hw_repository, dependencies.logger, dependencies.settings
        )
        asyncio.get_event_loop().run_until_complete(hot_wheels_scraper.run())

        logger.info("scraper.success")
        sys.exit(0)
    except HTTPError as e:
        logger.error("scraper.error", error=e)
    except FileNotFoundError as e:
        logger.error("scraper.file_not_found", error=e)

    sys.exit(1)
