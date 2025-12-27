# 1. Add HTTPException to the imports
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_user, require_admin
from app.core.database import SessionLocal
from app.dto import staff as schemas 
from app.services.staff import StaffService 

router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.StaffRead])
def read_staff(db: Session = Depends(get_db)):
    return StaffService.get_all_staff(db)

@router.post("/", response_model=schemas.StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(staff_in: schemas.StaffCreate, current_user=Depends(require_admin), db: Session = Depends(get_db)):
    return StaffService.create_staff_member(db, staff_in)

# --- NEW ENDPOINTS BELOW ---

@router.get("/{staff_id}", response_model=schemas.StaffRead)
def read_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    """Get a specific staff member by their ID."""
    staff = StaffService.get_staff_by_id(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(staff_id: int, current_user=Depends(require_admin), db: Session = Depends(get_db)):
    """Delete a staff member by their ID."""
    success = StaffService.delete_staff(db, staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return None