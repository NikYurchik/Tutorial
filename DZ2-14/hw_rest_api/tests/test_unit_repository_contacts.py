import os

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactResponse, UserModel, UserDb, UserResponse, TokenModel, RequestEmail
from src.repository.contacts import (
    get_contacts,
    get_contacts_by_mask,
    get_birthday_contacts,
    get_contact_by_id,
    create,
    update,
    remove
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
    #     if not os.path.exists("logs"):
    #         os.mkdir("logs")
    #     return super().setUpClass()

    def setUp(self):
        # self.logs = open(f"logs/{self._testMethodName}.log", mode="w", encoding="utf-8")
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    # def tearDown(self) -> None:
    #     self.logs.close()
    #     return super().tearDown()


    async def test_get_contacts(self):
        # try:
            contacts = [Contact(), Contact(), Contact(), Contact()]
            self.session.query().filter().limit().offset().all.return_value = contacts
            result = await get_contacts(offset=0, limit=10, user=self.user, db=self.session)
            self.assertEqual(result, contacts)
        #     self.logs.writelines("Test passed")
        # except Exception as err:
        #     self.logs.writelines("Test failed! result != contacts")
        #     self.logs.writelines(str(err))


    async def test_get_contacts_by_mask_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_contacts_by_mask(offset=0, limit=10, search_mask='search_mask', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_mask_notfound(self):
        contacts = []
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_contacts_by_mask(offset=0, limit=10, search_mask='search_mask', user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_get_birthday_contacts_found(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_birthday_contacts(offset=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_birthday_contacts_notfound(self):
        contacts = []
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_birthday_contacts(offset=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_get_contact_by_id_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_id_notfound(self):
        contact = None
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_create(self):
        body = ContactModel(first_name="first_name", last_name="last_name", email="test@mail.com", phone='0991234567', birthdate='2022-11-01')
        result = await create(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthdate, body.birthdate)
        self.assertTrue(hasattr(result, "id"))


    async def test_update_found(self):
        body = ContactModel(first_name="first_name", last_name="last_name", email="test@mail.com", phone='0991234567', birthdate='2022-11-01')
        contact = Contact(first_name="first_name", last_name="last_name", email="test@mail.com", phone='0991234567', birthdate='2022-11-01')
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_notfound(self):
        body = ContactModel(first_name="first_name", last_name="last_name", email="test@mail.com", phone='0991234567', birthdate='2022-11-01')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_remove_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_notfound(self):
        self.session.query().filter().first.return_value = None
        result = await remove(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)
