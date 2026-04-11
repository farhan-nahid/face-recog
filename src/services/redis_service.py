import time
from typing import Tuple, Optional
import redis
from core.settings import settings
from core.logging_config import logger

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


def check_redis_connection() -> Tuple[bool, Optional[float], Optional[str]]:
    """
    Check Redis connection status with retries.
    Retries up to 10 times with increasing delays: 1, 2, 4, 6, 8, ...
    """
    max_retries = 10
    last_error = None

    for i in range(max_retries):
        start_time = time.time()
        try:
            # ping() is a standard way to check Redis connectivity
            redis_client.ping()
            duration_ms = round((time.time() - start_time) * 1000, 1)
            if i > 0:
                logger.info(f"✅ Redis connected successfully on attempt {i + 1}")
            return True, duration_ms, None
        except Exception as e:
            last_error = str(e)
            if i < max_retries - 1:
                # Calculate delay: 1 for first retry, then 2, 4, 6, 8...
                delay = 1 if i == 0 else (i * 2)
                logger.warning(
                    f"⚠️ Redis connection attempt {i + 1} failed: {last_error}. Retrying in {delay}s..."
                )
                time.sleep(delay)
            else:
                logger.error(
                    f"❌ Redis connection failed after {max_retries} attempts: {last_error}"
                )

    return False, None, last_error
