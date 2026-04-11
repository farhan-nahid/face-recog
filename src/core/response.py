from typing import Any, Optional


def success_response(
    *,
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> dict:
    """
    Create a standardized success response.

    Args:
        data: The data payload to return.
        message: Success message description.

    Returns:
        dict: Standardized success response.
    """
    return {
        "status": "success",
        "status_code": status_code,
        "message": message,
        "data": data,
    }


def error_response(
    *,
    message: str,
    detail: Optional[str] = None,
    status_code: int = 400,
    error: Optional[str] = None,
) -> dict:
    """
    Create a standardized error response.

    Args:
        message: Error message description.
        detail: Optional error details.
        status_code: HTTP status code.
        error: Optional error code/name.

    Returns:
        dict: Standardized error response.
    """
    response = {
        "status": "failed",
        "error": error,
        "status_code": status_code,
        "message": message,
        "detail": detail,
    }
    return response
