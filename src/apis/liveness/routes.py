from fastapi import APIRouter, BackgroundTasks
from .schema import TemporarySessionCreateSchema
from core.schema import SuccessResponse, ErrorResponse
from .views import (
    create_temporary_credentials_view,
    create_liveness_session_view,
    get_liveness_session_result_view,
)


router = APIRouter(prefix="/api/v1/liveness", tags=["liveness"])


@router.post(
    "/temporary-credentials",
    response_model=SuccessResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def create_temporary_credentials(data: TemporarySessionCreateSchema):
    """
    Get temporary AWS credentials for frontend liveness detection.
    Returns credentials with limited permissions (only StartFaceLivenessSession).
    """
    return create_temporary_credentials_view(data.name)


@router.post(
    "",
    response_model=SuccessResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def create_liveness_session():
    """
    Create a new Face Liveness session.
    Returns a SessionId that should be used by the client SDK to start the liveness check.
    """
    return create_liveness_session_view()


@router.get(
    "/{session_id}/{collection_name}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def get_face_liveness_session_result(
    session_id: str,
    collection_name: str,
    background_tasks: BackgroundTasks,
    threshold: int = 80,
):
    """
    Retrieve specific results of a Face Liveness session.
    """
    return get_liveness_session_result_view(
        session_id, collection_name, background_tasks, threshold
    )


liveness_router = router
