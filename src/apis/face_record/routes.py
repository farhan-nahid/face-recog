from fastapi import APIRouter, Query, Path
from core.schema import SuccessResponse, ErrorResponse
from core.database import DbSession
from .views import (
    get_face_record_by_id_view,
    get_face_record_by_external_image_id_view,
    get_face_record_by_aws_face_id_view,
    get_face_records_by_employee_view,
    get_face_records_by_company_view,
    update_face_record_view,
    soft_delete_face_record_view,
    hard_delete_face_record_view,
    get_all_deleted_face_records_view,
    get_deleted_face_records_by_company_view,
    restore_face_record_view,
)
from .schema import FaceRecordUpdateSchema

# Constants
FACE_RECORD_UUID_DESC = "Face record UUID"
FACE_RECORD_NOT_FOUND_DESC = "Face record not found"
INTERNAL_SERVER_ERROR_DESC = "Internal server error"
COMPANY_ID_DESC = "Company ID"
MAX_RECORDS_DESC = "Maximum number of records (1-1000)"
OFFSET_DESC = "Number of records to skip"


router = APIRouter(prefix="/api/v1/face-record", tags=["face-record"])


@router.get(
    "/id/{record_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
    },
)
def get_face_record_by_id(
    db: DbSession,
    record_id: str = Path(..., description=FACE_RECORD_UUID_DESC),
):
    """
    Get a face record by its database ID.
    """
    return get_face_record_by_id_view(db, record_id)


@router.get(
    "/external/{aws_collection_id}/{external_image_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
    },
)
def get_face_record_by_external_image_id(
    db: DbSession,
    aws_collection_id: str = Path(..., description="AWS Collection ID"),
    external_image_id: str = Path(..., description="External image ID"),
):
    """
    Get a face record by external image ID and collection ID.
    """
    return get_face_record_by_external_image_id_view(
        db, external_image_id, aws_collection_id
    )


@router.get(
    "/aws-face/{aws_collection_id}/{aws_face_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
    },
)
def get_face_record_by_aws_face_id(
    db: DbSession,
    aws_collection_id: str = Path(..., description="AWS Collection ID"),
    aws_face_id: str = Path(..., description="AWS Face ID"),
):
    """
    Get a face record by AWS Face ID and collection ID.
    """
    return get_face_record_by_aws_face_id_view(db, aws_face_id, aws_collection_id)


@router.get(
    "/employee/{company_id}/{employee_id}",
    response_model=SuccessResponse,
)
def get_face_records_by_employee(
    db: DbSession,
    company_id: str = Path(..., description=COMPANY_ID_DESC),
    employee_id: str = Path(..., description="Employee ID"),
):
    """
    Get all face records for a specific employee.
    """
    return get_face_records_by_employee_view(db, company_id, employee_id)


@router.get(
    "/company/{company_id}",
    response_model=SuccessResponse,
)
def get_face_records_by_company(
    db: DbSession,
    company_id: str = Path(..., description=COMPANY_ID_DESC),
    limit: int = Query(100, ge=1, le=1000, description=MAX_RECORDS_DESC),
    offset: int = Query(0, ge=0, description=OFFSET_DESC),
):
    """
    Get all face records for a company with pagination.
    """
    return get_face_records_by_company_view(db, company_id, limit, offset)


@router.patch(
    "/{record_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_DESC},
    },
)
def update_face_record(
    db: DbSession,
    record_id: str = Path(..., description=FACE_RECORD_UUID_DESC),
    update_data: FaceRecordUpdateSchema = ...,
):
    """
    Update an existing face record.
    Allows partial updates of face record fields.
    """
    return update_face_record_view(db, record_id, update_data)


@router.delete(
    "/{record_id}",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_DESC},
    },
)
def soft_delete_face_record(
    db: DbSession,
    record_id: str = Path(..., description=FACE_RECORD_UUID_DESC),
):
    """
    Soft delete a face record by setting deleted_at timestamp.
    The record remains in the database but is marked as deleted.
    """
    return soft_delete_face_record_view(db, record_id)


@router.delete(
    "/{record_id}/permanent",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_DESC},
    },
)
def hard_delete_face_record(
    db: DbSession,
    record_id: str = Path(..., description=FACE_RECORD_UUID_DESC),
):
    """
    Permanently delete a face record from the database.
    ⚠️ WARNING: This operation cannot be undone!
    """
    return hard_delete_face_record_view(db, record_id)


@router.get(
    "/deleted",
    response_model=SuccessResponse,
)
def get_all_deleted_face_records(
    db: DbSession,
    limit: int = Query(100, ge=1, le=1000, description=MAX_RECORDS_DESC),
    offset: int = Query(0, ge=0, description=OFFSET_DESC),
):
    """
    Get all soft-deleted face records with pagination.
    """
    return get_all_deleted_face_records_view(db, limit, offset)


@router.get(
    "/deleted/company/{company_id}",
    response_model=SuccessResponse,
)
def get_deleted_face_records_by_company(
    db: DbSession,
    company_id: str = Path(..., description=COMPANY_ID_DESC),
    limit: int = Query(100, ge=1, le=1000, description=MAX_RECORDS_DESC),
    offset: int = Query(0, ge=0, description=OFFSET_DESC),
):
    """
    Get all soft-deleted face records for a specific company with pagination.
    """
    return get_deleted_face_records_by_company_view(db, company_id, limit, offset)


@router.post(
    "/{record_id}/restore",
    response_model=SuccessResponse,
    responses={
        404: {"model": ErrorResponse, "description": FACE_RECORD_NOT_FOUND_DESC},
        409: {
            "model": ErrorResponse,
            "description": "Employee already has active face record",
        },
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_DESC},
    },
)
def restore_face_record(
    db: DbSession,
    record_id: str = Path(..., description=FACE_RECORD_UUID_DESC),
):
    """
    Restore a soft-deleted face record.
    Validates that the employee doesn't already have an active face record.
    """
    return restore_face_record_view(db, record_id)


face_record_router = router
