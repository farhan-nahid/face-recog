from fastapi import APIRouter, Form, UploadFile, File
from core.schema import SuccessResponse, ErrorResponse
from core.validators import validate_image_file
from .views import recognize_face_view


router = APIRouter(prefix="/api/v1/recognition", tags=["recognition"])


@router.post(
    "",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "No face found in image"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    },
)
async def recognize_face(
    collection_name: str = Form(
        ...,
        min_length=3,
        max_length=255,
        description="Target collection name (3-255 characters)",
    ),
    threshold: int = Form(
        ..., ge=1, le=100, description="Similarity threshold for face recognition"
    ),
    file: UploadFile = File(..., description="Face image to recognize (JPEG/PNG)"),
):
    """
    Recognize faces in an image by searching a collection.
    Returns matching faces with similarity scores.
    """
    validate_image_file(file)
    image_bytes = await file.read()

    return recognize_face_view(
        collection_name=collection_name,
        image_bytes=image_bytes,
        threshold=threshold,
    )


recognition_router = router
