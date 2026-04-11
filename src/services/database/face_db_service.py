from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timezone
from core.models import FaceRecord
from core.logging_config import logger


class FaceDbService:
    """Service for managing face records in the database."""

    def create_face_record(
        self,
        db: Session,
        company_id: str,
        employee_id: str,
        aws_face_id: str,
        aws_image_id: str,
        aws_collection_id: str,
        external_image_id: Optional[str] = None,
        image_url: Optional[str] = None,
        confidence: Optional[float] = None,
        meta_data: Optional[Dict[str, Any]] = None,
    ) -> FaceRecord:
        """
        Create a new face record in the database.

        Args:
            db: Database session
            company_id: Company identifier
            employee_id: Employee identifier
            aws_face_id: AWS Rekognition FaceId (required)
            aws_image_id: AWS Image ID (required)
            aws_collection_id: AWS Rekognition CollectionId (required)
            external_image_id: External image identifier
            image_url: URL of the stored image
            confidence: Face detection confidence score
            meta_data: Additional metadata as JSON

        Returns:
            FaceRecord: Created face record
        """
        try:
            face_record = FaceRecord(
                company_id=company_id,
                employee_id=employee_id,
                aws_face_id=aws_face_id,
                aws_collection_id=aws_collection_id,
                external_image_id=external_image_id,
                aws_image_id=aws_image_id,
                image_url=image_url,
                confidence=confidence,
                meta_data=meta_data,
            )

            db.add(face_record)
            db.commit()
            db.refresh(face_record)

            logger.info(
                f"Created face record {face_record.id} for employee {employee_id}"
            )
            return face_record

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create face record: {str(e)}")
            raise

    def get_face_record_by_id(
        self, db: Session, record_id: str
    ) -> Optional[FaceRecord]:
        """
        Get a face record by its database ID.

        Args:
            db: Database session
            record_id: Face record UUID

        Returns:
            FaceRecord or None
        """
        try:
            return (
                db.query(FaceRecord)
                .filter(
                    and_(FaceRecord.id == record_id, FaceRecord.deleted_at.is_(None))
                )
                .first()
            )
        except Exception as e:
            logger.error(f"Failed to get face record by ID {record_id}: {str(e)}")
            return None

    def get_face_record_by_external_image_id(
        self, db: Session, external_image_id: str, aws_collection_id: str
    ) -> Optional[FaceRecord]:
        """
        Get a face record by external image ID and Collection ID.

        Args:
            db: Database session
            external_image_id: External image identifier
            aws_collection_id: AWS Rekognition CollectionId
        Returns:
            FaceRecord or None
        """
        try:
            return (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.external_image_id == external_image_id,
                        FaceRecord.aws_collection_id == aws_collection_id,
                        FaceRecord.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as e:
            logger.error(
                f"Failed to get face record by external image ID {external_image_id}: {str(e)}"
            )
            return None

    def get_face_record_by_aws_face_id(
        self, db: Session, aws_face_id: str, aws_collection_id: str
    ) -> Optional[FaceRecord]:
        """
        Get a face record by AWS Face ID and Collection ID.

        Args:
            db: Database session
            aws_face_id: AWS Rekognition FaceId
            aws_collection_id: AWS Rekognition CollectionId

        Returns:
            FaceRecord or None
        """
        try:
            return (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.aws_face_id == aws_face_id,
                        FaceRecord.aws_collection_id == aws_collection_id,
                        FaceRecord.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as e:
            logger.error(
                f"Failed to get face record by AWS Face ID {aws_face_id}: {str(e)}"
            )
            return None

    def get_face_record_by_aws_image_id(
        self, db: Session, aws_image_id: str, aws_collection_id: str
    ) -> Optional[FaceRecord]:
        """
        Get a face record by AWS Image ID and Collection ID.

        Args:
            db: Database session
            aws_image_id: AWS Image ID
            aws_collection_id: AWS Rekognition CollectionId

        Returns:
            FaceRecord or None
        """
        try:
            return (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.aws_image_id == aws_image_id,
                        FaceRecord.aws_collection_id == aws_collection_id,
                        FaceRecord.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as e:
            logger.error(
                f"Failed to get face record by AWS Image ID {aws_image_id}: {str(e)}"
            )
            return None

    def get_face_records_by_employee(
        self, db: Session, company_id: str, employee_id: str
    ) -> List[FaceRecord]:
        """
        Get all face records for a specific employee.

        Args:
            db: Database session
            company_id: Company identifier
            employee_id: Employee identifier

        Returns:
            List of FaceRecord objects
        """
        try:
            return (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.company_id == company_id,
                        FaceRecord.employee_id == employee_id,
                        FaceRecord.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as e:
            logger.error(
                f"Failed to get face records for employee {employee_id}: {str(e)}"
            )
            return []

    def get_face_records_by_company(
        self, db: Session, company_id: str, limit: int = 100, offset: int = 0
    ) -> List[FaceRecord]:
        """
        Get all face records for a company with pagination.

        Args:
            db: Database session
            company_id: Company identifier
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of FaceRecord objects
        """
        try:
            return (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.company_id == company_id,
                        FaceRecord.deleted_at.is_(None),
                    )
                )
                .limit(limit)
                .offset(offset)
                .all()
            )
        except Exception as e:
            logger.error(
                f"Failed to get face records for company {company_id}: {str(e)}"
            )
            return []

    def update_face_record(
        self,
        db: Session,
        record_id: str,
        aws_face_id: Optional[str] = None,
        aws_image_id: Optional[str] = None,
        image_url: Optional[str] = None,
        confidence: Optional[float] = None,
        meta_data: Optional[Dict[str, Any]] = None,
    ) -> Optional[FaceRecord]:
        """
        Update an existing face record.

        Args:
            db: Database session
            record_id: Face record UUID
            aws_face_id: New AWS Face ID (if face was re-indexed)
            aws_image_id: New AWS Image ID
            image_url: New image URL
            confidence: New confidence score
            meta_data: Updated metadata

        Returns:
            Updated FaceRecord or None
        """
        try:
            face_record = self.get_face_record_by_id(db, record_id)
            if not face_record:
                logger.warning(f"Face record {record_id} not found for update")
                return None

            if aws_face_id is not None:
                face_record.aws_face_id = aws_face_id
            if aws_image_id is not None:
                face_record.aws_image_id = aws_image_id
            if image_url is not None:
                face_record.image_url = image_url
            if confidence is not None:
                face_record.confidence = confidence
            if meta_data is not None:
                face_record.meta_data = meta_data

            db.commit()
            db.refresh(face_record)

            logger.info(f"Updated face record {record_id}")
            return face_record

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update face record {record_id}: {str(e)}")
            raise

    def soft_delete_face_record(self, db: Session, record_id: str) -> bool:
        """
        Soft delete a face record by setting deleted_at timestamp.

        Args:
            db: Database session
            record_id: Face record UUID

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            face_record = self.get_face_record_by_id(db, record_id)
            if not face_record:
                logger.warning(f"Face record {record_id} not found for deletion")
                return False

            face_record.deleted_at = datetime.now(timezone.utc)
            db.commit()

            logger.info(f"Soft deleted face record {record_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to soft delete face record {record_id}: {str(e)}")
            raise

    def soft_delete_by_aws_face_id(
        self, db: Session, aws_face_id: str, aws_collection_id: str
    ) -> bool:
        """
        Soft delete a face record by AWS Face ID.

        Args:
            db: Database session
            aws_face_id: AWS Rekognition FaceId
            aws_collection_id: AWS Rekognition CollectionId

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            face_record = self.get_face_record_by_aws_face_id(
                db, aws_face_id, aws_collection_id
            )
            if not face_record:
                logger.warning(
                    f"Face record with AWS Face ID {aws_face_id} not found for deletion"
                )
                return False

            face_record.deleted_at = datetime.now(timezone.utc)
            db.commit()

            logger.info(f"Soft deleted face record with AWS Face ID {aws_face_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(
                f"Failed to soft delete face record by AWS Face ID {aws_face_id}: {str(e)}"
            )
            raise

    def hard_delete_face_record(self, db: Session, record_id: str) -> bool:
        """
        Permanently delete a face record from the database.
        Use with caution - this cannot be undone.

        Args:
            db: Database session
            record_id: Face record UUID

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            face_record = (
                db.query(FaceRecord).filter(FaceRecord.id == record_id).first()
            )
            if not face_record:
                logger.warning(f"Face record {record_id} not found for hard deletion")
                return False

            db.delete(face_record)
            db.commit()

            logger.info(f"Hard deleted face record {record_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to hard delete face record {record_id}: {str(e)}")
            raise

    def get_all_deleted_face_records(
        self, db: Session, limit: int = 100, offset: int = 0
    ) -> List[FaceRecord]:
        """
        Get all soft-deleted face records with pagination.

        Args:
            db: Database session
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List[FaceRecord]: List of deleted face records
        """
        try:
            face_records = (
                db.query(FaceRecord)
                .filter(FaceRecord.deleted_at.isnot(None))
                .order_by(FaceRecord.deleted_at.desc())
                .limit(limit)
                .offset(offset)
                .all()
            )

            logger.info(f"Retrieved {len(face_records)} deleted face records")
            return face_records

        except Exception as e:
            logger.error(f"Failed to retrieve deleted face records: {str(e)}")
            raise

    def get_deleted_face_records_by_company(
        self, db: Session, company_id: str, limit: int = 100, offset: int = 0
    ) -> List[FaceRecord]:
        """
        Get all soft-deleted face records for a specific company with pagination.

        Args:
            db: Database session
            company_id: Company identifier
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List[FaceRecord]: List of deleted face records
        """
        try:
            face_records = (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.company_id == company_id,
                        FaceRecord.deleted_at.isnot(None),
                    )
                )
                .order_by(FaceRecord.deleted_at.desc())
                .limit(limit)
                .offset(offset)
                .all()
            )

            logger.info(
                f"Retrieved {len(face_records)} deleted face records for company {company_id}"
            )
            return face_records

        except Exception as e:
            logger.error(
                f"Failed to retrieve deleted face records for company {company_id}: {str(e)}"
            )
            raise

    def has_active_face_record(
        self, db: Session, company_id: str, employee_id: str
    ) -> bool:
        """
        Check if an employee has any active (non-deleted) face records.

        Args:
            db: Database session
            company_id: Company identifier
            employee_id: Employee identifier

        Returns:
            bool: True if employee has active face records, False otherwise
        """
        try:
            active_record = (
                db.query(FaceRecord)
                .filter(
                    and_(
                        FaceRecord.company_id == company_id,
                        FaceRecord.employee_id == employee_id,
                        FaceRecord.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return active_record is not None

        except Exception as e:
            logger.error(
                f"Failed to check active face records for employee {employee_id}: {str(e)}"
            )
            raise

    def restore_face_record(self, db: Session, record_id: str) -> Optional[FaceRecord]:
        """
        Restore a soft-deleted face record by clearing the deleted_at timestamp.

        Args:
            db: Database session
            record_id: Face record UUID

        Returns:
            Optional[FaceRecord]: Restored face record or None if not found
        """
        try:
            face_record = (
                db.query(FaceRecord)
                .filter(
                    and_(FaceRecord.id == record_id, FaceRecord.deleted_at.isnot(None))
                )
                .first()
            )

            if not face_record:
                logger.warning(
                    f"Deleted face record {record_id} not found for restoration"
                )
                return None

            face_record.deleted_at = None
            db.commit()
            db.refresh(face_record)

            logger.info(f"Restored face record {record_id}")
            return face_record

        except Exception as e:
            db.rollback()
            logger.error(f"Failed to restore face record {record_id}: {str(e)}")
            raise
