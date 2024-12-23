import logging
import sys
from typing import Annotated

import structlog
from fastapi import Depends
from structlog.contextvars import merge_contextvars
from structlog.stdlib import BoundLogger
from structlog import get_logger as get_struct_logger

from hot_wheels_collector.settings.base import is_local_env


LOGGER_NAME = "hw-collector"
render = (
    structlog.dev.ConsoleRenderer()
    if is_local_env()
    else structlog.processors.JSONRenderer()
)
# TODO(tm): fixme - debug lvl not working for local env as intended, setting DEBUG lvl for 3rd party libs
logger_level = logging.DEBUG if is_local_env() else logging.INFO


def configure_logger() -> BoundLogger:
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logger_level,
    )  # logging level for 3rd party libraries

    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper("iso"),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            render,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.getLogger("requests").setLevel(logging.CRITICAL)

    return get_struct_logger()


def get_logger() -> BoundLogger:
    return get_struct_logger()


LoggerDependency = Annotated[BoundLogger, Depends(get_logger)]
