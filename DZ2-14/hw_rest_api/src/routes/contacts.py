from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repos_contacts
from src.services.auth import auth_service
from src.conf import messages

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/",
            response_model=List[ContactResponse],
            description=messages.NO_MORE_THAN_10_REQUESTS_PER_MINUTE,
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts(limit: int = Query(10, le=50), offset: int = 0, search_mask: str = '', db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts.
    
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the maximum number of contacts returned
    :param offset: int: Specify the offset of the first contact to be returned
    :param search_mask: str: Search for contacts by mask
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    if not search_mask or search_mask == '*':
        # print('Get all contacts')
        contacts = await repos_contacts.get_contacts(limit, offset, current_user, db)
    else:
        # print(f'Search contacts by mask "{search_mask}"')
        contacts = await repos_contacts.get_contacts_by_mask(limit, offset, search_mask, current_user, db)
    return contacts


@router.get("/birthday",
            response_model=List[ContactResponse],
            description=messages.NO_MORE_THAN_10_REQUESTS_PER_MINUTE,
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_birthday_contacts(limit: int = Query(10, le=50), offset: int = 0, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_birthday_contacts function returns a list of contacts that have birthdays in the current month.
        The limit and offset parameters are used to paginate the results.
    
    
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned
    :param offset: int: Skip the first n contacts
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user_id from the database
    :return: A list of contacts that have a birthday on the current day
    :doc-author: Trelent
    """
    contacts = await repos_contacts.get_birthday_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}",
            response_model=ContactResponse,
            description=messages.NO_MORE_THAN_10_REQUESTS_PER_MINUTE,
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
        Args:
            - contact_id (int): The id of the contact to return.
            - db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            - current_user (User, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact_id from the path
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repos_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact


@router.post("/",
             response_model=ContactResponse, 
             status_code=status.HTTP_201_CREATED,
             description=messages.NO_MORE_THAN_10_REQUESTS_PER_MINUTE, 
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input, and returns the newly created contact.
    
    :param body: ContactModel: Pass the data that will be used to create a new contact
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :return: A contactmodel object, which is a pydantic model
    :doc-author: Trelent
    """
    contact = await repos_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}",
            response_model=ContactResponse,
            description=messages.NO_MORE_THAN_10_REQUESTS_PER_MINUTE, 
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        - The function takes an id, body and db as parameters.
        - It returns a ContactModel object.
    
    :param body: ContactModel: Define the body of the request
    :param contact_id: int: Get the id of the contact that we want to update
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the current user
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repos_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact


@router.delete("/{contact_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               description=messages.NO_MORE_THAN_10_REQUESTS_PER_MINUTE, 
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        Args:
            - contact_id (int): The id of the contact to be removed.\n
            - db (Session): A connection to the database.\n
            - current_user (User): The user who is making this request, as determined by auth_service's get_current_user function.
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repos_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
    return contact

