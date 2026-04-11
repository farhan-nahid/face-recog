from functools import wraps
from botocore.exceptions import ClientError
from fastapi import HTTPException
from core.logging_config import logger
from .errors import handle_aws_error


def aws_safe(func):
    """
    Decorator to handle AWS SDK errors gracefully.
    Catches ClientError exceptions and converts them to appropriate HTTP exceptions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            # Let HTTPException pass through without modification
            raise
        except ClientError as e:
            handle_aws_error(e)
        except Exception as e:
            # Log unexpected errors before re-raising
            logger.error(
                f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True
            )
            raise

    return wrapper
