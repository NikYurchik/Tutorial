from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse, ContactModel, ContactBirthdateModel
from src.repository import contacts as repos_contacts

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=50), offset: int = 0, search_mask: str = '', db: Session = Depends(get_db)):
    if not search_mask or search_mask == '*':
        print('Get all contacts')
        contacts = await repos_contacts.get_contacts(limit, offset, db)
    else:
        print(f'Search contacts by mask "{search_mask}"')
        contacts = await repos_contacts.get_contacts_by_mask(limit, offset, search_mask, db)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse])
async def get_birthday_contacts(limit: int = Query(10, le=50), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repos_contacts.get_birthday_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repos_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repos_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repos_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repos_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.patch("/{contact_id}/birthdate", response_model=ContactResponse)
async def set_birthdate_contact(body: ContactBirthdateModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repos_contacts.set_birthdate(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
