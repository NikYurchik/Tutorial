from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repos_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse],
            description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(limit: int = Query(10, le=50), offset: int = 0, search_mask: str = '', db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    if not search_mask or search_mask == '*':
        # print('Get all contacts')
        contacts = await repos_contacts.get_contacts(limit, offset, current_user, db)
    else:
        # print(f'Search contacts by mask "{search_mask}"')
        contacts = await repos_contacts.get_contacts_by_mask(limit, offset, search_mask, current_user, db)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse],
            description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_birthday_contacts(limit: int = Query(10, le=50), offset: int = 0, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repos_contacts.get_birthday_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse,
            description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repos_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repos_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse,
            description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repos_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT,
               description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repos_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact

