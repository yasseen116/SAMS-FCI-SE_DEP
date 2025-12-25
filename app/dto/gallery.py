from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class GalleryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Gallery item title")
    description: Optional[str] = Field(None, description="Optional description")
    alt_text: Optional[str] = Field(None, max_length=255, description="Alt text for accessibility")
    is_featured: bool = Field(False, description="Mark as featured item")
    

class GalleryCreateDTO(GalleryBase):
    created_by: Optional[str] = Field(None, max_length=100, description="Creator's identifier")


class GalleryUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    alt_text: Optional[str] = Field(None, max_length=255)
    is_featured: Optional[bool] = None


class GalleryResponseDTO(GalleryBase):
    id: int
    media_url: str
    created_by: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True