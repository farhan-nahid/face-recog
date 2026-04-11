from fastapi import APIRouter, HTTPException
from core.database import check_db_connection
from services.redis_service import check_redis_connection
from core.response import success_response, error_response
from core.schema import SuccessResponse


router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("", response_model=SuccessResponse)
def read_health():
    return success_response(message="AWS Face Recognition Service is healthy.")


@router.get("/liveness", response_model=SuccessResponse)
async def liveness():
    """Check if the service is alive and running."""
    return success_response(message="Service is alive")


@router.get("/readiness", response_model=SuccessResponse)
async def readiness():
    """Check if the service is ready (database and Redis connections)."""
    db_success, db_duration, db_error = check_db_connection()
    redis_success, redis_duration, redis_error = check_redis_connection()

    if not db_success or not redis_success:
        errors = []
        if not db_success:
            errors.append(f"Database: {db_error or 'Connection failed'}")
        if not redis_success:
            errors.append(f"Redis: {redis_error or 'Connection failed'}")

        raise HTTPException(
            status_code=503,
            detail=error_response(
                message=f"Service is not ready: {'; '.join(errors)}",
                status_code=503,
                error="ServiceNotReady",
            ),
        )

    return success_response(
        message=f"Service is ready. DB: {db_duration}ms, Redis: {redis_duration}ms"
    )


health_router = router
