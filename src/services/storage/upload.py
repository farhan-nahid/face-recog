from typing import Any, Dict

import requests

from core.settings import settings


def upload_image_api(
    image_bytes: bytes,
    file_name: str,
    path: str,
) -> Dict[str, Any]:
    """Upload image bytes to the storage API and return the JSON response."""
    response = requests.post(
        f"{settings.HR_API_URL}/v1/storage/",
        files={
            "file": (file_name, image_bytes, "image/jpeg"),
            "path": (None, path, "text/plain"),
        },
        headers={
            "Content-Type": "multipart/form-data",
            "x-internal-service-token": f"Bearer {settings.STORAGE_API_TOKEN}",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def upload_liveness_failed_image(
    image_bytes: bytes,
    session_id: str,
) -> Dict[str, Any]:
    """Upload failed liveness image via storage API and return the API payload."""
    return upload_image_api(
        image_bytes=image_bytes,
        file_name=f"{session_id}.jpg",
        path="liveness-failed-images/",
    )
