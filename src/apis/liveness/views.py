from core.response import success_response
from services.aws.liveness_service import create_session, get_session_results
from services.aws.sts_service import create_temporary_credentials
from fastapi import BackgroundTasks
from services.database.liveness_db_service import LivenessDbService
from core.database import SessionLocal


def create_liveness_session_view():
    response = create_session()

    return success_response(
        message="Liveness session created successfully", status_code=200, data=response
    )


def store_liveness_result_task(
    session_id: str,
    confidence: float,
    status: str,
    user_id: str = None,
    face_id: str = None,
    image_id: str = None,
    image_url: str = None,
    recognition_confidence: float = None,
    similarity: float = None,
    match_count: int = None,
):
    """Background task to store liveness result in the database."""
    db = SessionLocal()
    try:
        db_service = LivenessDbService()
        db_service.create_liveness_result(
            db=db,
            session_id=session_id,
            confidence=confidence,
            status=status,
            user_id=user_id,
            face_id=face_id,
            image_id=image_id,
            image_url=image_url,
            recognition_confidence=recognition_confidence,
            similarity=similarity,
            match_count=match_count,
        )
    finally:
        db.close()


def get_liveness_session_result_view(
    session_id: str,
    collection_name: str,
    background_tasks: BackgroundTasks,
    threshold: int = 80,
):
    response = get_session_results(session_id, collection_name, threshold)

    # Store result in background
    liveness_data = response.get("data", {}).get("liveness", {})
    recognition_response = response.get("data", {}).get("recognition", {})
    recognition_data = (
        recognition_response.get("data", {}) if recognition_response else {}
    )

    background_tasks.add_task(
        store_liveness_result_task,
        session_id=session_id,
        confidence=liveness_data.get("confidence"),
        status=liveness_data.get("status"),
        user_id=recognition_data.get("user_id"),
        face_id=recognition_data.get("face_id"),
        image_id=recognition_data.get("image_id"),
        image_url=liveness_data.get("image_url"),
        recognition_confidence=recognition_data.get("confidence"),
        similarity=recognition_data.get("best_match_similarity"),
        match_count=recognition_data.get("match_count"),
    )

    return success_response(
        message="Liveness session result retrieved successfully",
        status_code=200,
        data=response,
    )


def create_temporary_credentials_view(name: str):
    """Get temporary AWS credentials for frontend liveness detection."""
    result = create_temporary_credentials(name)

    return success_response(
        message="Temporary credentials generated successfully",
        status_code=200,
        data=result,
    )
