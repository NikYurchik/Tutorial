from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=30)
    email: EmailStr
    phone: str
    birthdate: date


class ContactBirthdateModel(BaseModel):
    birthdate: date


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthdate: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
