from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from .client import rekognition_client
from .decorators import aws_safe
from core.response import error_response


@aws_safe
def recognize_face(
    collection_name: str, image_bytes: bytes, threshold: int = 80
) -> Dict[str, Any]:
    """
    Search for matching faces in a collection using AWS Rekognition's
    SearchFacesByImage API

    Args:
        collection_name: Target collection to search in.
        image_bytes: Raw image bytes (JPEG/PNG) containing the face to recognize.
        threshold: Similarity score threshold (0-100). Default: 80.

    Returns:
        dict: Structured data containing user_data, schedule_data, searched face bounding box, best match similarity, and match count.

    Raises:
        HTTPException:
            - 404 if no face is detected in the image or if no matches are found above the similarity threshold.
    """
    response = rekognition_client.search_faces_by_image(
        CollectionId=collection_name,
        Image={"Bytes": image_bytes},
        FaceMatchThreshold=threshold,
    )
    face_matches: List[Dict[str, Any]] = response.get("FaceMatches", []) or []
    searched_face: Optional[Dict[str, Any]] = response.get("SearchedFaceBoundingBox")

    # No detectable face at all in the provided image
    if not searched_face and not face_matches:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message="No face found in the provided image",
                status_code=404,
                error="NoFaceDetected",
            ),
        )

    # No matches found above the given threshold
    if not face_matches:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message="No matching faces found above the similarity threshold",
                status_code=404,
                error="NoMatchesFound",
            ),
        )

    # Sort matches by similarity (descending) for convenience
    face_matches = sorted(
        face_matches, key=lambda x: x.get("Similarity", 0.0), reverse=True
    )

    # Select the best match (highest similarity)
    best_match = face_matches[0]
    user_id = best_match["Face"]["ExternalImageId"]

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail=error_response(
                message="Invalid user_id from best match",
                status_code=400,
                error="InvalidMatch",
            ),
        )

    data = {
        "user_id": user_id,
        "face_id": best_match.get("Face", {}).get("FaceId"),
        "image_id": best_match.get("Face", {}).get("ImageId"),
        "confidence": best_match.get("Face", {}).get("Confidence"),
        "best_match_similarity": best_match.get("Similarity"),
        "match_count": len(face_matches),
    }

    return {"data": data}
