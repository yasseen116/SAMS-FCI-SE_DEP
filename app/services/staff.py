from sqlalchemy.orm import Session
# FIX: Import from models, not database
from app.models.staff import StaffMember 
from app.dto.staff import StaffCreate

class StaffService:
    @staticmethod
    def get_all_staff(db: Session):
        return db.query(StaffMember).all()

    @staticmethod
    def create_staff_member(db: Session, staff_data: StaffCreate):
        new_staff = StaffMember(
            name=staff_data.name,
            position=staff_data.position,
            email=staff_data.email,
            photo_url=staff_data.photo_url
        )
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        return new_staff
    
    @staticmethod
    def get_staff_by_id(db: Session, staff_id: int):
        """Fetches a single staff member by ID."""
        return db.query(StaffMember).filter(StaffMember.id == staff_id).first()

    @staticmethod
    def delete_staff(db: Session, staff_id: int):
        """Deletes a staff member by ID. Returns True if deleted, False if not found."""
        staff = db.query(StaffMember).filter(StaffMember.id == staff_id).first()
        if staff:
            db.delete(staff)
            db.commit()
            return True
        return False