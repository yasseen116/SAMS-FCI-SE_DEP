from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.gallery import Gallery


class GalleryService:
    @staticmethod
    def list_gallery(
        session: Session, featured_only: bool = False, limit: int = 20, offset: int = 0
    ) -> List[Gallery]:
        query = session.query(Gallery)

        if featured_only:
            query = query.filter(Gallery.is_featured == True)

        query = query.order_by(Gallery.created_at.desc())
        query = query.limit(limit).offset(offset)

        return query.all()

    @staticmethod
    def get_gallery_item(session:Session, item_id: int) -> Optional[Gallery]:
        return session.query(Gallery).filter(Gallery.id == item_id).first()
    
    @staticmethod
    def create_gallery_item(session:Session, data: dict) -> Gallery:
        gallery_item = Gallery(**data)
        session.add(gallery_item)
        session.commit()
        session.refresh(gallery_item)
        return gallery_item
    
    @staticmethod
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
    def delete_gallery_item(session:Session, item_id: int) -> bool:
        gallery_item = session.query(Gallery).filter(Gallery.id == item_id).first()
        if not gallery_item:
            return False
        
        session.delete(gallery_item)
        session.commit()
        return True
        