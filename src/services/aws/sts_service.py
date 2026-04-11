import json
from datetime import datetime, timezone
from core.settings import settings
from services.redis_service import redis_client
from .decorators import aws_safe
from .client import sts_client


@aws_safe
def create_temporary_credentials(name: str = "liveness-session"):
    """
    Generate temporary AWS credentials with limited permissions for face liveness.
    Uses Redis to cache credentials and avoid frequent STS calls.
    """
    # Using structured key
    cache_key = f"prod:ak:face:v1:sts:{name}"

    # Try to get from cache
    try:
        cached_creds_json = redis_client.get(cache_key)
        if cached_creds_json:
            cached_creds = json.loads(cached_creds_json)
            # Check if expiration is at least 60 seconds away
            expiration_str = cached_creds.get("expiration")
            if expiration_str:
                expiration = datetime.fromisoformat(expiration_str)
                if (expiration - datetime.now(timezone.utc)).total_seconds() > 60:
                    return {"data": cached_creds}
    except Exception as e:
        # Fallback to AWS if Redis fails
        from core.logging_config import logger

        logger.warning(f"Redis cache access failed in STS service: {str(e)}")

    # Policy that only allows starting face liveness sessions
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["rekognition:StartFaceLivenessSession"],
                "Resource": "*",
            }
        ],
    }

    # Get temporary credentials using federation token
    duration = settings.AWS_STS_DURATION_SECONDS
    response = sts_client.get_federation_token(
        Name=name,
        Policy=json.dumps(policy),
        DurationSeconds=duration,
    )

    credentials = response.get("Credentials", {})
    expiration = credentials.get("Expiration")

    creds_data = {
        "access_key_id": credentials.get("AccessKeyId"),
        "secret_access_key": credentials.get("SecretAccessKey"),
        "session_token": credentials.get("SessionToken"),
        "expiration": expiration.isoformat() if expiration else None,
        "region": settings.AWS_REGION,
    }

    # Cache in Redis with TTL (slightly less than duration to be safe)
    if expiration:
        try:
            ttl = int((expiration - datetime.now(timezone.utc)).total_seconds()) - 10
            if ttl > 0:
                redis_client.setex(cache_key, ttl, json.dumps(creds_data))
        except Exception as e:
            from core.logging_config import logger

            logger.warning(f"Failed to set Redis cache in STS service: {str(e)}")

    return {"data": creds_data}
