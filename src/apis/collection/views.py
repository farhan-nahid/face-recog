from core.response import success_response
from services.aws import (
    create_collection,
    get_all_collections,
    get_collection,
    delete_collection,
)


def create_collection_view(name: str):
    """
    Create a new AWS Rekognition collection.

    This view function handles the creation of a new face recognition collection
    in AWS Rekognition. Each collection is isolated and can store faces for
    face recognition and comparison.

    Args:
        name: Unique identifier for the collection (typically company_uuid)

    Returns:
        dict: Success response with collection details including ARN and status

    Raises:
        HTTPException: 409 if collection already exists
                      400 if collection name is invalid
    """
    result = create_collection(name)

    return success_response(
        message="Collection created successfully",
        data=result["data"],
        status_code=201,
    )


def get_all_collections_view():
    """
    Retrieve all AWS Rekognition collections.

    This view function fetches a list of all available face recognition collections
    in the configured AWS Rekognition account. Useful for managing multiple
    company collections or auditing.

    Returns:
        dict: Success response with list of collection IDs and face model versions
    """
    result = get_all_collections()

    return success_response(
        message="Collections retrieved successfully",
        data=result["data"],
    )


def get_collection_view(collection_name: str):
    """
    Retrieve details of a specific AWS Rekognition collection.

    This view function fetches detailed information about a specific collection
    including face count, ARN, creation timestamp, and face model version.

    Args:
        collection_name: Unique identifier of the collection to retrieve

    Returns:
        dict: Success response with collection metadata

    Raises:
        HTTPException: 404 if collection not found
                      400 if collection name is invalid
    """
    result = get_collection(collection_name)

    return success_response(
        message="Collection retrieved successfully",
        data=result["data"],
    )


def delete_collection_view(collection_name: str):
    """
    Delete an AWS Rekognition collection.

    This view function permanently removes a face recognition collection from
    AWS Rekognition. All faces stored in this collection will be deleted.
    This operation is irreversible.

    WARNING: This will permanently delete all face data in the collection.

    Args:
        collection_name: Unique identifier of the collection to delete

    Returns:
        dict: Success response with deletion status code

    Raises:
        HTTPException: 404 if collection not found
                      400 if collection name is invalid
    """
    result = delete_collection(collection_name)

    return success_response(
        message="Collection deleted successfully",
        data=result["data"],
    )
