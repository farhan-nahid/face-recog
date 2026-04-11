from typing import Optional

from fastapi import HTTPException

from core.database import DbSession
from core.logging_config import logger
from core.response import error_response, success_response
from services.aws import add_face, delete_face, get_face_by_id, list_faces
from services.database import face_db_service


def add_face_view(
    db: DbSession,
    collection_name: str,
    image_bytes: bytes,
    external_image_id: str,
    image_url: str,
):
    """
    Add a face into the specified AWS Rekognition collection and save to database.
    """
    # Step 1: Retrieve the face record from database to get AWS Face ID
    face_record = face_db_service.get_face_record_by_external_image_id(
        db=db,
        external_image_id=external_image_id,
        aws_collection_id=collection_name,
    )

    if face_record:
        raise HTTPException(
            status_code=400,
            detail=error_response(
                message="Face with the given external_image_id already exists in the database",
                status_code=400,
                error="DuplicateRecord",
            ),
        )

    # Step 1: Add face to AWS Rekognition
    result = add_face(collection_name, image_bytes, external_image_id)

    # Step 2: Save face record to database
    try:
        face_record = face_db_service.create_face_record(
            db=db,
            company_id=collection_name,
            employee_id=external_image_id,
            aws_face_id=result["data"]["face_id"],
            aws_image_id=result["data"]["image_id"],
            aws_collection_id=collection_name,
            external_image_id=external_image_id,
            image_url=image_url,
            confidence=result["data"].get("confidence"),
        )
        logger.info(f"Face record saved to database with ID: {face_record.id}")
    except Exception as e:
        logger.error(f"Failed to save face record to database: {str(e)}")

    return success_response(message="Face added successfully", status_code=201)


def list_faces_view(
    collection_name: str, next_token: Optional[str] = None, limit: int = 1000
):
    result = list_faces(collection_name, next_token, limit)
    return success_response(
        message="Faces listed successfully",
        data=result["data"],
    )


def get_face_view(collection_name: str, face_id: str):
    result = get_face_by_id(collection_name, face_id)
    return success_response(
        message="Face retrieved successfully",
        data=result["data"],
    )


def update_face_view(
    db: DbSession,
    collection_name: str,
    external_image_id: str,
    image_bytes: bytes,
    image_url: str,
):
    """
    Update a face: Delete old face from AWS Rekognition , soft-delete DB record,
    then add new face to AWS Rekognition, and save new record to DB.
    """
    # Step 1: Retrieve the old face record from database
    old_face_record = face_db_service.get_face_record_by_external_image_id(
        db=db,
        external_image_id=external_image_id,
        aws_collection_id=collection_name,
    )
    if not old_face_record:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message="Face with the given external_image_id not found in the database",
                status_code=404,
                error="ResourceNotFound",
            ),
        )

    old_face_id = old_face_record.aws_face_id

    # Step 2: Delete old face from AWS Rekognition
    try:
        delete_face(collection_name, old_face_id)
        logger.info(f"Old face deleted from AWS Rekognition: {old_face_id}")
    except Exception as e:
        logger.error(f"Failed to delete old face from AWS Rekognition: {str(e)}")
        # Continue with update even if AWS delete fails

    # Step 3: Soft delete old face record from database
    try:
        deleted = face_db_service.soft_delete_by_aws_face_id(
            db=db,
            aws_face_id=old_face_id,
            aws_collection_id=collection_name,
        )
        if deleted:
            logger.info(
                f"Old face record soft-deleted from database for AWS Face ID: {old_face_id}"
            )
        else:
            logger.warning(
                f"No database record found for soft deletion of AWS Face ID: {old_face_id}"
            )
    except Exception as e:
        logger.error(f"Failed to soft delete old face record from database: {str(e)}")

    # Step 4: Add new face to AWS Rekognition
    try:
        add_result = add_face(collection_name, image_bytes, external_image_id)
    except Exception as e:
        logger.error(f"Failed to add updated face to AWS Rekognition: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(
                message="Failed to add updated face to AWS Rekognition",
                status_code=500,
                error="InternalServerError",
            ),
        )

    meta_data = {
        "old_aws_face_id": old_face_record.aws_face_id,
        "old_aws_image_id": old_face_record.aws_image_id,
        "old_image_url": old_face_record.image_url,
        "old_record_soft_deleted": deleted,
    }

    # Step 7: Save new face record to database with metadata
    try:
        new_face_record = face_db_service.create_face_record(
            db=db,
            company_id=collection_name,
            employee_id=external_image_id,
            aws_face_id=add_result["data"]["face_id"],
            aws_image_id=add_result["data"]["image_id"],
            aws_collection_id=collection_name,
            external_image_id=external_image_id,
            image_url=image_url,
            confidence=add_result["data"].get("confidence"),
            meta_data=meta_data,
        )

        logger.info(
            f"New face record saved to database with ID: {new_face_record.id} and metadata"
        )
    except Exception as e:
        logger.error(f"Failed to save new face record to database: {str(e)}")

    return success_response(message="Face updated successfully")


def delete_face_view(
    db: DbSession,
    collection_name: str,
    external_image_id: str,
):
    """
    Delete a face from AWS Rekognition and soft-delete database record.
    """
    # Step 1: Retrieve the face record from database to get AWS Face ID
    face_record = face_db_service.get_face_record_by_external_image_id(
        db=db,
        external_image_id=external_image_id,
        aws_collection_id=collection_name,
    )

    if not face_record:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message="Face not found in database",
                status_code=404,
                error="ResourceNotFound",
            ),
        )

    face_id = face_record.aws_face_id

    # Step 2: Delete face from AWS Rekognition
    result = delete_face(collection_name, face_id)

    # Step 3: Soft delete face record from database
    try:
        deleted = face_db_service.soft_delete_by_aws_face_id(
            db=db,
            aws_face_id=face_id,
            aws_collection_id=collection_name,
        )
        if deleted:
            result["data"]["db_record_deleted"] = True
            logger.info(
                f"Face record soft-deleted from database for AWS Face ID: {face_id}"
            )
        else:
            result["data"]["db_record_deleted"] = False
            logger.warning(f"No database record found for AWS Face ID: {face_id}")
    except Exception as e:
        logger.error(f"Failed to soft delete face record from database: {str(e)}")
        result["data"]["db_delete_error"] = str(e)

    return success_response(
        message="Face deleted successfully",
        data=result["data"],
    )


def delete_face_aws_view(collection_name: str, face_id: str):
    """
    Delete a face from AWS Rekognition only (without touching database).
    """
    result = delete_face(collection_name, face_id)
    return success_response(
        message="Face deleted from AWS Rekognition successfully",
        data=result["data"],
    )
