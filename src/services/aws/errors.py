from fastapi import HTTPException
from botocore.exceptions import ClientError
from core.response import error_response
from core.logging_config import logger


def handle_aws_error(e: ClientError) -> None:
    """
    Handle AWS ClientError and raise appropriate HTTPException.

    Args:
        e: The ClientError exception from boto3.

    Raises:
        HTTPException: With appropriate status code and detail message.
    """
    error = e.response["Error"]
    code = error["Code"]
    message = error.get("Message", "AWS Error")
    request_id = e.response.get("ResponseMetadata", {}).get("RequestId")
    http_status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    # Log the full error details for debugging
    logger.error(
        f"AWS ClientError: Code={code}, Message={message}, "
        f"RequestId={request_id}, HTTPStatus={http_status}"
    )

    error_map = {
        "ResourceAlreadyExistsException": (409, "Resource already exists"),
        "ResourceNotFoundException": (404, "Resource not found"),
        "InvalidParameterException": (400, "Invalid parameters provided"),
        "AccessDeniedException": (403, "Access denied to AWS resource"),
        "InvalidS3ObjectException": (400, "Invalid S3 object"),
        "InvalidImageFormatException": (400, "Invalid image format"),
        "ImageTooLargeException": (413, "Image file too large"),
        "ProvisionedThroughputExceededException": (429, "Rate limit exceeded"),
        "ThrottlingException": (429, "Request throttled"),
        "InternalServerError": (500, "Internal server error"),
    }

    status_code, default_message = error_map.get(code, (500, message))

    raise HTTPException(
        status_code=status_code,
        detail=error_response(
            message=default_message,
            detail=message if default_message != message else None,
            status_code=status_code,
            error=code,
        ),
    )
