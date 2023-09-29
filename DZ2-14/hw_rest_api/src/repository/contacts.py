from datetime import datetime

from sqlalchemy import between, and_, or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Get the contacts from a certain point in the database
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contacts_by_mask(limit: int, offset: int, search_mask:str, user: User, db: Session):
    """
    The get_contacts_by_mask function returns a list of contacts that match the search_mask.
        - The function takes in limit, offset, and search_mask parameters to determine which contacts to return.
        - It also takes in a user parameter so it can only return contacts belonging to that user.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :param search_mask:str: Filter the contacts by first name, last name or email
    :param user: User: Get the user's id and use it to filter out contacts that belong to other users
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).\
                filter(and_(Contact.user_id == user.id, or_(Contact.first_name.like(search_mask), Contact.last_name.like(search_mask), Contact.email.like(search_mask)))).\
                limit(limit).offset(offset).all()
    return contacts


async def get_birthday_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The get_birthday_contacts function returns a list of contacts whose birthday is within the next 7 days.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before returning any
    :param user: User: Pass the user object to the function
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    cdt = datetime.now().date()
    doy = cdt - cdt.replace(day=1, month=1)
    doy = doy.days
    contacts = db.query(Contact).\
                filter(and_(Contact.user_id == user.id, between(Contact.days_of_year, doy, doy + 7))).\
                limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on the user_id and contact_id.
        Args:
            - contact_id (int): The id of the desired Contact object.\n
            - user (User): The User object that owns this Contact.\n
            - db (Session): A Session instance to connect to our database with.
    
    :param contact_id: int: Specify the id of the contact to be retrieved from the database
    :param user: User: Get the user_id of the logged in user
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    return contact


async def create(body: ContactModel, user: User, db: Session):
    """
    The create function creates a new contact in the database.
    
    :param body: ContactModel: Pass in the contact information that is being created
    :param user: User: Get the user_id from the jwt token
    :param db: Session: Pass in the database session to the function
    :return: A contact, so the response should be a contactmodel
    :doc-author: Trelent
    """
    # contact = Contact(**body.dict(), user_id=user.id)
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone, birthdate=body.birthdate, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update function updates a contact in the database.
    
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactModel: Pass the data from the request body to update function
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A contact, but the response is not a contactmodel
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthdate = body.birthdate
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    """
    The remove function removes a contact from the database.
    
    :param contact_id: int: Specify the contact to be removed
    :param user: User: Get the user_id of the current user
    :param db: Session: Pass the database session to the function
    :return: A contact object, so we can use it to return a 404 if the contact doesn't exist
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

