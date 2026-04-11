from pydantic import BaseModel, Field


class TemporarySessionCreateSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Collection name (3-255 characters)",
    )
