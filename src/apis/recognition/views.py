from core.response import success_response
from services.aws import recognize_face


def recognize_face_view(collection_name: str, image_bytes: bytes, threshold: int = 80):
    """
    Recognize faces in an image by searching a collection.
    """
    result = recognize_face(collection_name, image_bytes, threshold)

    return success_response(
        message="Face recognition completed",
        data=result["data"],
    )
