from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.file_handler import FileHandler
from app.dto.gallery import GalleryResponseDTO, GalleryUpdateDTO
from app.services.gallery import GalleryService

router = APIRouter(prefix="/gallery", tags=["gallery"])

# List gallery items with optional filtering for featured items
@router.get("/", response_model=List[GalleryResponseDTO])
def list_gallery(
    featured_only: bool = Query(False, description="Filter to only featured items"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Items to skip"),
    session: Session = Depends(get_session)  # ← Fixed from get_db
):
    
    items = GalleryService.list_gallery(session, featured_only, limit, offset)
    return items

# Get a single gallery item by ID
@router.get("/{item_id}", response_model=GalleryResponseDTO)
def get_gallery_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    
    item = GalleryService.get_gallery_item(session, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery item with id {item_id} not found"
        )
    return item

# Create a new gallery item with image upload
@router.post("/", response_model=GalleryResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_gallery_item(
    file: UploadFile = File(..., description="Image file"),
    title: str = Form(..., description="Gallery item title"),
    description: Optional[str] = Form(None),
    alt_text: Optional[str] = Form(None),
    is_featured: bool = Form(False),
    created_by: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
 
   
    try:
        media_url = await FileHandler.save_upload_file(file, "app/uploads/gallery")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    
    gallery_data = {
        "title": title,
        "description": description,
        "media_url": media_url,
        "alt_text": alt_text,
        "is_featured": is_featured,
        "created_by": created_by
    }
    
    try:
        item = GalleryService.create_gallery_item(session, gallery_data)
        return item
    except Exception as e:
       
        FileHandler.delete_file(media_url)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create gallery item: {str(e)}"
        )

# Update an existing gallery item
@router.put("/{item_id}", response_model=GalleryResponseDTO)
def update_gallery_item(
    item_id: int,
    data: GalleryUpdateDTO,
    session: Session = Depends(get_session)
):
    
    update_data = data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
    item = GalleryService.update_gallery_item(session, item_id, update_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery item with id {item_id} not found"
        )
    return item


# Delete a gallery item by ID
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery_item(
    item_id: int,
    session: Session = Depends(get_session)
):  
    
    item = GalleryService.get_gallery_item(session, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery item with id {item_id} not found"
        )
    
    
    file_deleted = FileHandler.delete_file(str(item.media_url))
    if not file_deleted:
        print(f"Warning: File not found for deletion: {item.media_url}")
    
    
    success = GalleryService.delete_gallery_item(session, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete gallery item from database"
        )
    
    return None