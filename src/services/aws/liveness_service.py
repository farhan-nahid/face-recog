import io

from .client import rekognition_client
from .face_recognition_service import recognize_face
from .decorators import aws_safe
from services.storage.upload import upload_liveness_failed_image


@aws_safe
def create_session():
    """
    Create a Face Liveness session.

    Args:
        client_request_token (str, optional): A unique token to identify the session.

    Returns:
        dict: The response from create_face_liveness_session.
    """
    settings = {
        "AuditImagesLimit": 3,
        "ChallengePreferences": [
            {
                "Type": "FaceMovementAndLightChallenge",
            },
        ],
    }

    response = rekognition_client.create_face_liveness_session(Settings=settings)

    return {"data": {"session_id": response.get("SessionId")}}


@aws_safe
def get_session_results(session_id: str, collection_name: str, threshold: int = 80):
    """
    Get the results of a Face Liveness session.

    Args:
        session_id (str): The ID of the session.
        collection_name (str): The name of the face collection.
        threshold (int, optional): The confidence threshold for face recognition. Defaults to 80.
    Returns:
        dict: The results of the session, including confidence and status.
    """
    response = rekognition_client.get_face_liveness_session_results(
        SessionId=session_id,
    )

    confidence = response.get("Confidence", 0)
    status = response.get("Status", "FAILED")
    reference_image_bytes = response.get("ReferenceImage", {}).get("Bytes")

    image_url = None
    is_failed = confidence < threshold or status != "SUCCEEDED"
    if is_failed and reference_image_bytes:
        upload_result = upload_liveness_failed_image(
            image_bytes=reference_image_bytes,
            session_id=session_id,
        )
        upload_data = upload_result.get("data", {})
        image_url = upload_data.get("file_url")

    if confidence < threshold:
        return {
            "data": {
                "liveness": {
                    "session_id": response.get("SessionId"),
                    "status": status,
                    "confidence": confidence,
                    "image_url": image_url,
                },
                "recognition": None,
            }
        }

    if "ReferenceImage" not in response:
        return {
            "data": {
                "liveness": {
                    "session_id": response.get("SessionId"),
                    "status": status,
                    "confidence": confidence,
                    "image_url": image_url,
                },
                "recognition": None,
            }
        }

    image_stream = io.BytesIO(response["ReferenceImage"]["Bytes"])
    recognition = recognize_face(
        collection_name=collection_name,
        image_bytes=image_stream.getvalue(),
        threshold=threshold,
    )

    return {
        "data": {
            "liveness": {
                "session_id": response.get("SessionId"),
                "status": status,
                "confidence": confidence,
                "image_url": image_url,
            },
            "recognition": recognition,
        }
    }
