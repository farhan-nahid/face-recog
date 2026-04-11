from pydantic import BaseModel, Field, field_validator
import re


class CollectionCreateSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Collection name (3-255 characters)",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Collection name must match AWS Rekognition requirements."""
        if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
            raise ValueError(
                "Collection name can only contain alphanumeric characters, underscores, and hyphens"
            )
        return v
