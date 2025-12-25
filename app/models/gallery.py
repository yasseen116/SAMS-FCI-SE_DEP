from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, Text
from sqlalchemy.sql import func

from .base import Base


# Gallery model representing a gallery item in the database.
class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    media_url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    alt_text = Column(String(255), nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        Index('ix_gallery_is_featured', 'is_featured'),
        Index("ix_gallery_created_at", "created_at"),
    )