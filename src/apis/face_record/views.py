from fastapi import HTTPException
from core.response import success_response, error_response
from core.database import DbSession
from core.logging_config import logger
from core.models import FaceRecord
from services.database import face_db_service
from .schema import FaceRecordUpdateSchema

# Constants
FACE_RECORD_RETRIEVED_MSG = "Face record retrieved successfully"
FACE_RECORD_NOT_FOUND_MSG = "Face record not found"


def face_record_to_dict(face_record: FaceRecord) -> dict:
    """Convert FaceRecord model to dictionary for JSON serialization."""
    return {
        "id": str(face_record.id),
        "company_id": face_record.company_id,
        "employee_id": face_record.employee_id,
        "external_image_id": face_record.external_image_id,
        "aws_collection_id": face_record.aws_collection_id,
        "aws_image_id": face_record.aws_image_id,
        "aws_face_id": face_record.aws_face_id,
        "image_url": face_record.image_url,
        "confidence": face_record.confidence,
        "meta_data": face_record.meta_data,
        "created_at": face_record.created_at.isoformat()
        if face_record.created_at
        else None,
        "updated_at": face_record.updated_at.isoformat()
        if face_record.updated_at
        else None,
        "deleted_at": face_record.deleted_at.isoformat()
        if face_record.deleted_at
        else None,
    }


def get_face_record_by_id_view(db: DbSession, record_id: str):
    """
    Get a face record by its database ID.

    Args:
        db: Database session
        record_id: Face record UUID

    Returns:
        dict: Success response with face record data

    Raises:
        HTTPException: 404 if record not found
    """
    face_record = face_db_service.get_face_record_by_id(db, record_id)

    if not face_record:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message=FACE_RECORD_NOT_FOUND_MSG,
                status_code=404,
                error="ResourceNotFound",
            ),
        )

    return success_response(
        message=FACE_RECORD_RETRIEVED_MSG,
        data=face_record_to_dict(face_record),
    )


def get_face_record_by_external_image_id_view(
    db: DbSession, external_image_id: str, aws_collection_id: str
):
    """
    Get a face record by external image ID and collection ID.

    Args:
        db: Database session
        external_image_id: External image identifier
        aws_collection_id: AWS collection ID

    Returns:
        dict: Success response with face record data

    Raises:
        HTTPException: 404 if record not found
    """
    face_record = face_db_service.get_face_record_by_external_image_id(
        db, external_image_id, aws_collection_id
    )

    if not face_record:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message=FACE_RECORD_NOT_FOUND_MSG,
                status_code=404,
                error="ResourceNotFound",
            ),
        )

    return success_response(
        message=FACE_RECORD_RETRIEVED_MSG,
        data=face_record_to_dict(face_record),
    )


def get_face_record_by_aws_face_id_view(
    db: DbSession, aws_face_id: str, aws_collection_id: str
):
    """
    Get a face record by AWS Face ID and collection ID.

    Args:
        db: Database session
        aws_face_id: AWS Face ID
        aws_collection_id: AWS collection ID

    Returns:
        dict: Success response with face record data

    Raises:
        HTTPException: 404 if record not found
    """
    face_record = face_db_service.get_face_record_by_aws_face_id(
        db, aws_face_id, aws_collection_id
    )

    if not face_record:
        raise HTTPException(
            status_code=404,
            detail=error_response(
                message=FACE_RECORD_NOT_FOUND_MSG,
                status_code=404,
                error="ResourceNotFound",
            ),
        )

    return success_response(
        message=FACE_RECORD_RETRIEVED_MSG,
        data=face_record_to_dict(face_record),
    )


def get_face_records_by_employee_view(db: DbSession, company_id: str, employee_id: str):
    """
    Get all face records for a specific employee.

    Args:
        db: Database session
        company_id: Company identifier
        employee_id: Employee identifier

    Returns:
        dict: Success response with list of face records
    """
    face_records = face_db_service.get_face_records_by_employee(
        db, company_id, employee_id
    )

    records_data = [face_record_to_dict(record) for record in face_records]

    return success_response(
        message="Face records retrieved successfully",
        data={
            "records": records_data,
            "total": len(records_data),
        },
    )


def get_face_records_by_company_view(
    db: DbSession, company_id: str, limit: int = 100, offset: int = 0
):
    """
    Get all face records for a company with pagination.

    Args:
        db: Database session
        company_id: Company identifier
        limit: Maximum number of records to return
        offset: Number of records to skip

    Returns:
        dict: Success response with paginated list of face records
    """
    face_records = face_db_service.get_face_records_by_company(
        db, company_id, limit, offset
    )

    records_data = [face_record_to_dict(record) for record in face_records]

    return success_response(
        message="Face records retrieved successfully",
        data={
            "records": records_data,
            "total": len(records_data),
            "limit": limit,
            "offset": offset,
        },
    )


def update_face_record_view(
    db: DbSession, record_id: str, update_data: FaceRecordUpdateSchema
):
    """
    Update an existing face record.

    Args:
        db: Database session
        record_id: Face record UUID
        update_data: Update data schema

    Returns:
        dict: Success response with updated face record

    Raises:
        HTTPException: 404 if record not found
    """
    try:
        updated_record = face_db_service.update_face_record(
            db=db,
            record_id=record_id,
            aws_face_id=update_data.aws_face_id,
            aws_image_id=update_data.aws_image_id,
            image_url=update_data.image_url,
            confidence=update_data.confidence,
            meta_data=update_data.meta_data,
        )

        if not updated_record:
            raise HTTPException(
                status_code=404,
                detail=error_response(
                    message=FACE_RECORD_NOT_FOUND_MSG,
                    status_code=404,
                    error="ResourceNotFound",
                ),
            )

        return success_response(
            message="Face record updated successfully",
            data=face_record_to_dict(updated_record),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update face record {record_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(
                message="Failed to update face record",
                status_code=500,
                error="InternalServerError",
            ),
        )


def soft_delete_face_record_view(db: DbSession, record_id: str):
    """
    Soft delete a face record by setting deleted_at timestamp.

    Args:
        db: Database session
        record_id: Face record UUID

    Returns:
        dict: Success response with deletion status

    Raises:
        HTTPException: 404 if record not found
    """
    try:
        deleted = face_db_service.soft_delete_face_record(db, record_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=error_response(
                    message=FACE_RECORD_NOT_FOUND_MSG,
                    status_code=404,
                    error="ResourceNotFound",
                ),
            )

        return success_response(
            message="Face record soft deleted successfully",
            data={"record_id": record_id, "deleted": True},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to soft delete face record {record_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(
                message="Failed to delete face record",
                status_code=500,
                error="InternalServerError",
            ),
        )


def hard_delete_face_record_view(db: DbSession, record_id: str):
    """
    Permanently delete a face record from the database.
    Use with caution - this cannot be undone.

    Args:
        db: Database session
        record_id: Face record UUID

    Returns:
        dict: Success response with deletion status

    Raises:
        HTTPException: 404 if record not found
    """
    try:
        deleted = face_db_service.hard_delete_face_record(db, record_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=error_response(
                    message=FACE_RECORD_NOT_FOUND_MSG,
                    status_code=404,
                    error="ResourceNotFound",
                ),
            )

        return success_response(
            message="Face record permanently deleted",
            data={"record_id": record_id, "deleted": True},
            status_code=200,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to hard delete face record {record_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(
                message="Failed to delete face record",
                status_code=500,
                error="InternalServerError",
            ),
        )


def get_all_deleted_face_records_view(db: DbSession, limit: int = 100, offset: int = 0):
    """
    Get all soft-deleted face records with pagination.

    Args:
        db: Database session
        limit: Maximum number of records to return
        offset: Number of records to skip

    Returns:
        dict: Success response with paginated list of deleted face records
    """
    face_records = face_db_service.get_all_deleted_face_records(db, limit, offset)

    records_data = [face_record_to_dict(record) for record in face_records]

    return success_response(
        message="Deleted face records retrieved successfully",
        data={
            "records": records_data,
            "total": len(records_data),
            "limit": limit,
            "offset": offset,
        },
    )


def get_deleted_face_records_by_company_view(
    db: DbSession, company_id: str, limit: int = 100, offset: int = 0
):
    """
    Get all soft-deleted face records for a company with pagination.

    Args:
        db: Database session
        company_id: Company identifier
        limit: Maximum number of records to return
        offset: Number of records to skip

    Returns:
        dict: Success response with paginated list of deleted face records
    """
    face_records = face_db_service.get_deleted_face_records_by_company(
        db, company_id, limit, offset
    )

    records_data = [face_record_to_dict(record) for record in face_records]

    return success_response(
        message="Deleted face records retrieved successfully",
        data={
            "records": records_data,
            "total": len(records_data),
            "limit": limit,
            "offset": offset,
        },
    )


def restore_face_record_view(db: DbSession, record_id: str):
    """
    Restore a soft-deleted face record.
    Validates that the employee doesn't have any active face records before restoring.

    Args:
        db: Database session
        record_id: Face record UUID

    Returns:
        dict: Success response with restored face record

    Raises:
        HTTPException: 404 if record not found
                      409 if employee already has active face record
                      500 if restore operation fails
    """
    try:
        # First, get the deleted record to check company_id and employee_id
        deleted_record = face_db_service.get_face_record_by_id(db, record_id)

        if not deleted_record:
            raise HTTPException(
                status_code=404,
                detail=error_response(
                    message=FACE_RECORD_NOT_FOUND_MSG,
                    status_code=404,
                    error="ResourceNotFound",
                ),
            )

        # Check if the record is actually deleted
        if deleted_record.deleted_at is None:
            raise HTTPException(
                status_code=400,
                detail=error_response(
                    message="Face record is not deleted",
                    status_code=400,
                    error="BadRequest",
                ),
            )

        # Check if employee has any active face records
        has_active = face_db_service.has_active_face_record(
            db, deleted_record.company_id, deleted_record.employee_id
        )

        if has_active:
            raise HTTPException(
                status_code=409,
                detail=error_response(
                    message="Cannot restore: Employee already has an active face record",
                    status_code=409,
                    error="ConflictError",
                ),
            )

        # Restore the record
        restored_record = face_db_service.restore_face_record(db, record_id)

        if not restored_record:
            raise HTTPException(
                status_code=404,
                detail=error_response(
                    message="Face record not found or could not be restored",
                    status_code=404,
                    error="ResourceNotFound",
                ),
            )

        return success_response(
            message="Face record restored successfully",
            data=face_record_to_dict(restored_record),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to restore face record {record_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=error_response(
                message="Failed to restore face record",
                status_code=500,
                error="InternalServerError",
            ),
        )
