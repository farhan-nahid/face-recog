from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any


class FaceRecordUpdateSchema(BaseModel):
    """Schema for updating face record"""

    aws_face_id: Optional[str] = Field(None, description="AWS Face ID")
    aws_image_id: Optional[str] = Field(None, description="AWS Image ID")
    image_url: Optional[str] = Field(None, description="Image URL")
    confidence: Optional[float] = Field(
        None, ge=0, le=100, description="Confidence score (0-100)"
    )
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: Optional[float]) -> Optional[float]:
        """Validate confidence is within valid range."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Confidence must be between 0 and 100")
        return v
