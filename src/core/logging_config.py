from loguru import logger
import sys
from enum import Enum

# Python 3.11+ compatibility: StrEnum
# For Python 3.9-3.10, we create a simple alternative
try:
    from enum import StrEnum
except ImportError:
    # Fallback for Python < 3.11
    class StrEnum(str, Enum):
        """String Enum compatibility for Python < 3.11"""

        pass


class LogLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def configure_logging(log_level: str = LogLevels.INFO) -> None:
    # Remove default Loguru handler
    logger.remove()

    # Format template for HTTP request logs
    # Includes all request context with color coding
    # Using a custom format function to handle optional fields
    def request_formatter(record):
        extra = record["extra"]
        parts = [
            f"<green>{record['time']:YYYY-MM-DD HH:mm:ss}</green>",
            f"<level>{record['level'].name: <8}</level>",
        ]

        # Add request fields if present
        if "request_id" in extra:
            parts.append(f"<blue>{extra['request_id']: <10}</blue>")
        if "method" in extra:
            parts.append(f"<magenta>{extra['method']: <6}</magenta>")
        if "route" in extra:
            parts.append(f"<cyan>{extra['route']: <30}</cyan>")
        if "status" in extra:
            parts.append(f"<yellow>{extra['status']: <3}</yellow>")
        if "duration" in extra:
            parts.append(f"<white>{extra['duration']: >6}ms</white>")
        if "ip" in extra:
            parts.append(f"<green>{extra['ip']: <15}</green>")
        if "user_agent" in extra:
            agent = str(extra["user_agent"])[:30]
            parts.append(f"<dim>{agent}</dim>")

        parts.append(f"{record['message']}")
        return " | ".join(parts) + "\n"

    # Format template for general application logs
    # Simple format without request context
    simple_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
        "| <level>{level: <8}</level> "
        "| {message}"
    )

    # Handler for HTTP request logs
    # Only processes logs that include request_id in extra data
    logger.add(
        sys.stdout,
        level=log_level,
        format=request_formatter,
        filter=lambda record: "request_id" in record["extra"],
        colorize=True,
    )

    # Handler for general application logs
    # Processes logs that don't include request context
    logger.add(
        sys.stdout,
        level=log_level,
        format=simple_format,
        filter=lambda record: "request_id" not in record["extra"],
        colorize=True,
    )

    logger.info("Logging configured successfully.")
