"""
Common Pydantic schemas used across all API endpoints.
"""

from pydantic import BaseModel
from typing import Optional, Any


class SuccessResponse(BaseModel):
    """Standardized success response format for all endpoints."""

    status: str = "success"
    status_code: int = 200
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standardized error response format for all endpoints."""

    status: str = "failed"
    error: Optional[str] = None
    status_code: int
    message: str
    detail: Optional[str] = None
