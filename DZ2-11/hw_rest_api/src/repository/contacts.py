from datetime import datetime

from sqlalchemy import between
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contacts_by_mask(limit: int, offset: int, search_mask:str, db: Session):
    contacts = db.query(Contact).\
                filter((Contact.first_name.like(search_mask)) | (Contact.last_name.like(search_mask)) | (Contact.email.like(search_mask))).\
                limit(limit).offset(offset).all()
    return contacts


async def get_birthday_contacts(limit: int, offset: int, db: Session):
    cdt = datetime.now().date()
    doy = cdt - cdt.replace(day=1, month=1)
    doy = doy.days
    contacts = db.query(Contact).\
                filter(between(Contact.days_of_year, doy, doy + 7)).\
                limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(cat_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=cat_id).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthdate = body.birthdate
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

