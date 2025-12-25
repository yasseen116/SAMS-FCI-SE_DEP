from pydantic import BaseModel, EmailStr
from typing import Optional

class StaffBase(BaseModel):
    name: str # [cite: 204]
    position: str # [cite: 204]
    email: str # [cite: 206]
    photo_url: Optional[str] = None # [cite: 204]

class StaffCreate(StaffBase):
    pass  # Used for POST requests

class StaffRead(StaffBase):
    id: int

    class Config:
        from_attributes = True