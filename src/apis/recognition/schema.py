from pydantic import BaseModel, Field, field_validator
import re


class FaceRecognizeFormParams(BaseModel):
    """Form parameters for recognizing a face (multipart/form-data)"""

    collection_name: str = Field(
        ..., min_length=3, max_length=255, description="Target collection to search in"
    )
    threshold: int = Field(
        80,
        ge=0,
        le=100,
        description="Similarity threshold (0-100). Only return matches above this score.",
    )

    @field_validator("collection_name")
    @classmethod
    def validate_collection_name(cls, v: str) -> str:
        """Collection name must match AWS Rekognition requirements."""
        if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
            raise ValueError(
                "Collection name can only contain alphanumeric characters, underscores, and hyphens"
            )
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "collection_name": "my_company_collection",
                "threshold": 80,
            }
        }
