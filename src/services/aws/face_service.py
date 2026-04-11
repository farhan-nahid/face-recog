from typing import Optional
from fastapi import HTTPException
from .client import rekognition_client
from .decorators import aws_safe
from core.response import error_response


@aws_safe
def add_face(collection_name: str, image_bytes: bytes, external_image_id: str):
    """
    Add a face to an AWS Rekognition collection using raw image bytes.

    Args:
        collection_name: Target collection name.
        image_bytes: Raw image bytes (JPEG/PNG).
        external_image_id: ExternalImageId to associate with the face (e.g., user_uuid).

    Returns:
        dict: Data with FaceId and ExternalImageId.

    Raises:
        HTTPException: 404 if no face is detected.
    """
    response = rekognition_client.index_faces(
        CollectionId=collection_name,
        Image={"Bytes": image_bytes},
        # User-friendly ID (e.g., user_uuid)
        ExternalImageId=external_image_id,
        QualityFilter="AUTO",  # Automatically filter low-quality faces
    )

    # Extract indexed face records from AWS response
    face_records = response.get("FaceRecords", [])
    if not face_records:
        # No face detected in the image
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message="No faces found in the image",
                status_code=404,
                error="NoFacesFound",
            ),
        )

    # Extract data from first face record (one image = one face per call)
    face = face_records[0]["Face"]
    return {
        "data": {
            "face_id": face.get("FaceId"),  # AWS-generated unique ID
            "image_id": face.get("ImageId"),  # AWS image ID
            "confidence": face.get("Confidence"),  # Confidence score
            # User-provided ID
            "external_image_id": face.get("ExternalImageId"),
        }
    }


@aws_safe
def list_faces(
    collection_name: str, next_token: Optional[str] = None, max_results: int = 1000
):
    """List faces in a collection (paginated).

    Retrieves all faces in the specified collection with pagination support.
    AWS returns a maximum of max_results faces per request.
    """
    # Build parameters for ListFaces API call
    params = {"CollectionId": collection_name}

    # Add pagination token if provided (for fetching subsequent pages)
    if next_token:
        params["NextToken"] = next_token

    # Set maximum number of results per page
    if max_results:
        params["MaxResults"] = max_results

    # Call AWS Rekognition ListFaces API
    response = rekognition_client.list_faces(**params)

    return {
        "data": {
            "faces": response.get("Faces", []),  # List of face records
            # Token for next page (if exists)
            "next_token": response.get("NextToken"),
        }
    }


@aws_safe
def get_face_by_id(collection_name: str, face_id: str):
    """Retrieve a single face record by `FaceId` in a collection.
    Rekognition has no direct DescribeFace API, so we paginate through ListFaces.
    """
    next_token = None

    # Loop through paginated results until we find the target face or reach the end
    while True:
        # Fetch one page of faces from the collection
        page = (
            rekognition_client.list_faces(
                CollectionId=collection_name, NextToken=next_token
            )
            if next_token
            else rekognition_client.list_faces(CollectionId=collection_name)
        )
        faces = page.get("Faces", [])

        # Search for the target face in this page
        for face in faces:
            if face.get("FaceId") == face_id:
                # Found it! Return the face record
                return {"data": face}

        # Move to next page if available
        next_token = page.get("NextToken")
        if not next_token:
            # No more pages - face not found
            break

    # Face not found in any page
    raise HTTPException(
        status_code=404,
        detail=error_response(
            message="Face not found in collection",
            status_code=404,
            error="ResourceNotFound",
        ),
    )


@aws_safe
def delete_face(collection_name: str, face_id: str):
    """Delete a single face by `FaceId`.

    Permanently removes a face from the collection. The face embedding
    is deleted and cannot be recovered.
    """
    # Call AWS DeleteFaces API with the face ID
    response = rekognition_client.delete_faces(
        CollectionId=collection_name, FaceIds=[face_id]
    )

    # Check if the face was successfully deleted
    deleted = response.get("DeletedFaces", [])
    if face_id in deleted:
        # Successfully deleted
        return {"data": {"deleted": True, "face_id": face_id}}

    # Face was not deleted - either not found or already removed
    raise HTTPException(
        status_code=404,
        detail=error_response(
            message="Face not found or already deleted",
            status_code=404,
            error="ResourceNotFound",
        ),
    )


@aws_safe
def update_face(
    collection_name: str, face_id: str, image_bytes: bytes, image_name: str
):
    """Update a face by deleting the old `FaceId` and indexing the new image.

    AWS Rekognition does not support in-place updates of face embeddings.
    Instead, we delete the old face and re-index with the new image.
    This generates a new FaceId.
    """
    # Step 1: Delete the old face from the collection
    # We wrap this in try-except because if the face doesn't exist, we still want to proceed
    try:
        rekognition_client.delete_faces(CollectionId=collection_name, FaceIds=[face_id])
    except Exception:
        # If delete fails (e.g., face already removed), we continue to re-index
        pass

    # Step 2: Index the new face image
    response = rekognition_client.index_faces(
        CollectionId=collection_name,
        Image={"Bytes": image_bytes},
        ExternalImageId=image_name,  # Can be same or different from old ID
        QualityFilter="AUTO",
    )

    # Check if new face was detected and indexed
    face_records = response.get("FaceRecords", [])
    if not face_records:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message="No faces found in the image",
                status_code=404,
                error="NoFacesFound",
            ),
        )

    # Extract the new face data
    face = face_records[0]["Face"]
    return {
        "data": {
            "new_face_id": face.get("FaceId"),  # New AWS-generated ID
            "new_image_id": face.get("ImageId"),  # New AWS image ID
            "confidence": face.get("Confidence"),  # Confidence score
            # User-provided ID
            "external_image_id": face.get("ExternalImageId"),
        }
    }
