from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from core.database import Base


class FaceRecord(Base):
    __tablename__ = "face_records"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
        index=True,
    )
    company_id = Column(String, nullable=False, index=True)
    employee_id = Column(String, nullable=False, index=True)
    external_image_id = Column(String, nullable=True, index=True)
    aws_collection_id = Column(String, nullable=False, index=True)
    aws_image_id = Column(String, nullable=False, index=True)
    aws_face_id = Column(String, nullable=False, index=True)
    image_url = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)


class LivenessResult(Base):
    __tablename__ = "liveness_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        unique=True,
        nullable=False,
        index=True,
    )
    session_id = Column(String, nullable=False, index=True)
    confidence = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    user_id = Column(String, nullable=True, index=True)
    face_id = Column(String, nullable=True, index=True)
    image_id = Column(String, nullable=True, index=True)
    image_url = Column(String, nullable=True)
    recognition_confidence = Column(Float, nullable=True)
    similarity = Column(Float, nullable=True)
    match_count = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)
