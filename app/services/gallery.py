from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.gallery import Gallery

# Service layer for gallery operations
class GalleryService:
    @staticmethod
    # List gallery items with optional filtering for featured items
    def list_gallery(
        session: Session, featured_only: bool = False, limit: int = 20, offset: int = 0
    ) -> List[Gallery]:
        query = session.query(Gallery)

        if featured_only:
            query = query.filter(Gallery.is_featured)

        query = query.order_by(Gallery.created_at.desc())
        query = query.limit(limit).offset(offset)

        return query.all()

    @staticmethod
    # Get a single gallery item by ID
    def get_gallery_item(session:Session, item_id: int) -> Optional[Gallery]:
        return session.query(Gallery).filter(Gallery.id == item_id).first()
    
    @staticmethod
    # Create a new gallery item
    def create_gallery_item(session: Session, data: dict) -> Gallery:
        gallery_item = Gallery(**data)
        session.add(gallery_item)
        session.commit()
        session.refresh(gallery_item)
        return gallery_item
    
    @staticmethod
    # Update an existing gallery item
    def update_gallery_item(session:Session, item_id: int, data: dict) -> Optional[Gallery]:
        gallery_item = session.query(Gallery).filter(Gallery.id == item_id).first()
        if not gallery_item:
            return None
        
        for key, value in data.items():
            setattr(gallery_item, key, value)
        
        session.commit()
        session.refresh(gallery_item)
        return gallery_item
    
    @staticmethod
    # Delete a gallery item by ID
    def delete_gallery_item(session:Session, item_id: int) -> bool:
        gallery_item = session.query(Gallery).filter(Gallery.id == item_id).first()
        if not gallery_item:
            return False
        
        session.delete(gallery_item)
        session.commit()
        return True
        