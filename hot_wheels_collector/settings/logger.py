from typing import Annotated

import structlog
from fastapi import Depends
from structlog.stdlib import BoundLogger
from structlog import get_logger as get_structlog_logger


def configure_logger() -> BoundLogger:
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.contextvars.merge_contextvars,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    return get_structlog_logger()


def get_logger() -> BoundLogger:
    return get_structlog_logger()


LoggerDependency = Annotated[BoundLogger, Depends(get_logger)]
