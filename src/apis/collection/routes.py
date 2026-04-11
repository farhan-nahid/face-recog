from fastapi import APIRouter
from .views import (
    create_collection_view,
    get_all_collections_view,
    get_collection_view,
    delete_collection_view,
)
from .schema import CollectionCreateSchema
from core.schema import SuccessResponse, ErrorResponse


router = APIRouter(prefix="/api/v1/collection", tags=["collection"])


@router.post(
    "",
    response_model=SuccessResponse,
    responses={
        409: {"model": ErrorResponse, "description": "Collection already exists"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    },
)
async def add_new_collection(data: CollectionCreateSchema):
    """
    Create a new collection in AWS Rekognition.
    """
    return create_collection_view(data.name)


@router.get(
    "",
    response_model=SuccessResponse,
)
async def get_collections():
    """
    Retrieve all collections from AWS Rekognition.
    """
    return get_all_collections_view()


@router.get(
    "/{collection_name}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Collection not found"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    },
)
async def get_a_collection(collection_name: str):
    """
    Retrieve a specific collection from AWS Rekognition.
    """
    return get_collection_view(collection_name)


@router.delete(
    "/{collection_name}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Collection not found"},
        400: {"model": ErrorResponse, "description": "Invalid parameters"},
    },
)
async def delete_an_collection(collection_name: str):
    """
    Delete a collection in AWS Rekognition.
    """
    return delete_collection_view(collection_name)


collection_router = router
