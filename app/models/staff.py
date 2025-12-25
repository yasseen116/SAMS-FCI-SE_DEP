from sqlalchemy import Column, Integer, String
from app.core.database import Base

class StaffMember(Base):
    __tablename__ = "staff_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) 
    position = Column(String, nullable=False)
    email = Column(String,  nullable=False) 
    photo_url = Column(String, nullable=True) 