"""
Common validation utilities for API requests.
"""

from fastapi import UploadFile, HTTPException
from core.response import error_response


def validate_image_file(file: UploadFile) -> None:
    """
    Validate that uploaded file is JPEG or PNG.

    Args:
        file: The uploaded file to validate.

    Raises:
        HTTPException: 400 if file type or extension is invalid.
    """
    allowed_mimes = {"image/jpeg", "image/png"}
    allowed_exts = {".jpg", ".jpeg", ".png"}

    content_type = file.content_type or ""
    filename = (file.filename or "").lower()

    if content_type not in allowed_mimes:
        raise HTTPException(
            status_code=400,
            detail=error_response(
                message="Invalid file type",
                detail="Only jpg, jpeg or png are allowed",
                status_code=400,
                error="UnsupportedMediaType",
            ),
        )

    if not any(filename.endswith(ext) for ext in allowed_exts):
        raise HTTPException(
            status_code=400,
            detail=error_response(
                message="Invalid file extension",
                detail="Only .jpg, .jpeg or .png are allowed",
                status_code=400,
                error="InvalidExtension",
            ),
        )
