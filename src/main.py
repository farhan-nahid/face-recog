from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import sys

# Load environment variables from .env file
load_dotenv()

from apis.health.routes import health_router  # noqa: E402
from apis.collection.routes import collection_router  # noqa: E402
from apis.face.routes import face_router  # noqa: E402
from apis.recognition.routes import recognition_router  # noqa: E402
from apis.face_record.routes import face_record_router  # noqa: E402
from apis.liveness.routes import liveness_router  # noqa: E402
from core.logging_middleware import logging_middleware  # noqa: E402
from core.logging_config import configure_logging, LogLevels, logger  # noqa: E402
from core.settings import settings  # noqa: E402
from core.database import check_db_connection  # noqa: E402
from services.redis_service import check_redis_connection  # noqa: E402


# Configure logging on startup
configure_logging(log_level=LogLevels.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Checking database connection...")
    success, duration_ms, error_msg = check_db_connection()

    if not success:
        logger.error(f"❌ Failed to connect to database: {error_msg}")
        logger.error("Exiting application due to database connection failure")
        sys.exit(1)

    logger.info(f"✅ Database connected successfully in {duration_ms}ms")
    logger.info(f"🚀 Initializing application on http://localhost:{settings.PORT}")

    # Redis Startup Check
    logger.info("Checking Redis connection...")
    redis_success, redis_duration_ms, redis_error_msg = check_redis_connection()

    if not redis_success:
        logger.error(f"❌ Failed to connect to Redis: {redis_error_msg}")
        # Not exiting for Redis as it's a cache, but logging clearly
    else:
        logger.info(f"✅ Redis connected successfully in {redis_duration_ms}ms")

    yield

    # Shutdown (cleanup if needed)
    logger.info("Application shutting down...")


app = FastAPI(
    lifespan=lifespan,
    root_path="/face-rec",  # Set root path for reverse proxy setups
)


# Add logging middleware FIRST to capture all requests
@app.middleware("http")
async def add_logging_middleware(request, call_next):
    return await logging_middleware(request, call_next)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS.split(","),
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_credentials=True,
    allow_headers=["Authorization", "Content-Type"],
)


app.include_router(health_router)
app.include_router(collection_router)
app.include_router(face_router)
app.include_router(liveness_router)
app.include_router(recognition_router)
app.include_router(face_record_router)
