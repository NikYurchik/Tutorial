from bson.objectid import ObjectId

from models import Contact

def contact_create(fullname: str, email: str=None, is_email: bool=False, phone: str=None, is_phone: bool=False):
    contact = Contact(fullname=fullname, email=email, is_email=is_email, phone=phone, is_phone=is_phone).save()
    return contact

def contsct_read(_id: str):
    contact = Contact.objects(pk=ObjectId(_id)).first()
    return contact

def contsct_find(fullname: str=None, email: str=None, is_email: bool=False, phone: str=None, is_phone: bool=False, is_send: bool=False):
    if fullname:
        contacts = Contact.objects(fullname=fullname)
    elif email:
        contacts = Contact.objects(email=email)
    elif is_email:
        contacts = Contact.objects(is_email=is_email)
    elif phone:
        contacts = Contact.objects(phone=phone)
    elif is_phone:
        contacts = Contact.objects(is_phone=is_phone)
    elif is_send:
        contacts = Contact.objects(is_send=is_send)
    else:
        contacts = Contact.objects()
    return contacts

def contact_count():
    count = Contact.objects().count()
    return count

def contact_set_send(_id: str, is_send: bool):
    contact = Contact.objects(pk=ObjectId(_id)).first()
    if contact:
        contact.update(
            fullname=contact.fullname,
            email=contact.email,
            is_email=contact.is_email,
            phone=contact.phone,
            is_phone=contact.is_phone,
            is_send=is_send
        )
    else:
        return False
    return True
