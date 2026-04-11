from fastapi import APIRouter, File, Form, Query, UploadFile

from core.database import DbSession
from core.schema import ErrorResponse, SuccessResponse
from core.validators import validate_image_file

from .views import (
    add_face_view,
    delete_face_aws_view,
    delete_face_view,
    get_face_view,
    list_faces_view,
    update_face_view,
)

router = APIRouter(prefix="/api/v1/face", tags=["face"])


@router.post(
    "",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "No faces found"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    },
)
async def add_face(
    db: DbSession,
    collection_name: str = Form(
        ...,
        min_length=3,
        max_length=255,
        description="Target collection name (3-255 characters)",
    ),
    external_image_id: str = Form(
        ...,
        min_length=1,
        max_length=255,
        description="External image ID (e.g., user_uuid)",
    ),
    image: UploadFile = File(..., description="Face image (JPEG/PNG)"),
    image_url: str = Form(
        ...,
        min_length=1,
        max_length=512,
        description="External image URL (must be a valid URL pointing to a JPEG/PNG image)",
    ),
):
    """
    Add a face to a specific collection using a file upload.
    Accepts JPEG/PNG images only. All parameters are sent in the request body as multipart/form-data.
    """
    validate_image_file(image)
    image_bytes = await image.read()

    return add_face_view(
        db=db,
        collection_name=collection_name,
        image_bytes=image_bytes,
        external_image_id=external_image_id,
        image_url=image_url,
    )


@router.get(
    "",
    response_model=SuccessResponse,
)
async def list_faces(
    collection_name: str = Query(..., description="Target collection name"),
    limit: int = Query(
        1000, ge=1, le=1000, description="Maximum number of faces to return (1-1000)"
    ),
    next_token: str | None = Query(
        None, description="Pagination token from previous response"
    ),
):
    return list_faces_view(collection_name, next_token, limit)


@router.get(
    "/{collection_name}/{face_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Face not found"},
    },
)
async def get_face(collection_name: str, face_id: str):
    """
    Retrieve a face by its `face_id` from the specified collection.
    """
    return get_face_view(collection_name, face_id)


@router.put(
    "/{collection_name}/{external_image_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "No faces found"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    },
)
async def update_face(
    db: DbSession,
    collection_name: str,
    external_image_id: str,
    image: UploadFile = File(..., description="New face image (JPEG/PNG)"),
    image_url: str = Form(
        ...,
        min_length=1,
        max_length=512,
        description="External image URL",
    ),
):
    """
    Update an existing face in a collection by replacing the image.
    Accepts JPEG/PNG images only.
    """
    validate_image_file(image)
    image_bytes = await image.read()
    return update_face_view(
        db=db,
        collection_name=collection_name,
        external_image_id=external_image_id,
        image_bytes=image_bytes,
        image_url=image_url,
    )


@router.delete(
    "/{collection_name}/{external_image_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Face not found"},
    },
)
async def delete_face(db: DbSession, collection_name: str, external_image_id: str):
    """
    Delete a face from AWS Rekognition and soft-delete database record.
    """
    return delete_face_view(db, collection_name, external_image_id)


@router.delete(
    "/{collection_name}/{face_id}/aws",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Face not found"},
    },
)
async def delete_face_aws(db: DbSession, collection_name: str, face_id: str):
    """
    Delete a face from AWS Rekognition only (without touching database).
    """
    return delete_face_aws_view(collection_name, face_id)


face_router = router
