class Contacts:
    current_id = 1

    def __init__(self):
        self.contacts = []

    def list_contacts(self):
        return self.contacts

    def add_contacts(self, name, phone, email, favorite):
        self.contacts.append({'id': Contacts.current_id,
                              'name': name,
                              'phone': phone,
                              'email': email,
                              'favorite': favorite
                             })
        Contacts.current_id += 1

    def get_contact_by_id(self, id):
        for v in filter(lambda x: x["id"] == id, self.contacts):
            return v
        return None

    def remove_contacts(self, id):
        res = list(filter(lambda contact: contact.get("id") == id, self.contacts))
        if len(res) > 0:
            try:
                self.contacts.remove(res[0])
            except:
                pass


# {'id': 1, 'name': 'Wylie Pope', 'phone': '(692) 802-2949', 'email': 'est@utquamvel.net', 'favorite': True}
# {'id': 2, 'name': 'Cyrus Jackson', 'phone': '(501) 472-5218', 'email': 'nibh@semsempererat.com', 'favorite': False}
# [{'id': 1, 'name': 'Wylie Pope', 'phone': '(692) 802-2949', 'email': 'est@utquamvel.net', 'favorite': True}, {'id': 2, 'name': 'Cyrus Jackson', 'phone': '(501) 472-5218', 'email': 'nibh@semsempererat.com', 'favorite': False}]

# {'id': 3, 'name': 'Wylie Pope', 'phone': '(692) 802-2949', 'email': 'est@utquamvel.net', 'favorite': False}
# {'id': 4, 'name': 'Cyrus Jackson', 'phone': '(501) 472-5218', 'email': 'nibh@semsempererat.com', 'favorite': False}
# [{'id': 3, 'name': 'Wylie Pope', 'phone': '(692) 802-2949', 'email': 'est@utquamvel.net', 'favorite': False}, {'id': 4, 'name': 'Cyrus Jackson', 'phone': '(501) 472-5218', 'email': 'nibh@semsempererat.com', 'favorite': False}]                
contact = Contacts()
contact.add_contacts('Wylie Pope', '(692) 802-2949', 'est@utquamvel.net', True)
contact.add_contacts('Cyrus Jackson', '(501) 472-5218', 'nibh@semsempererat.com', False)
print(contact.list_contacts())
print(contact.get_contact_by_id(2))
contact.remove_contacts(2)
print(contact.list_contacts())
print('------------------------------------------------------------------------')
contact2 = Contacts()
contact2.add_contacts('Wylie Pope', '(692) 802-2949', 'est@utquamvel.net', False)
contact2.add_contacts('Cyrus Jackson', '(501) 472-5218', 'nibh@semsempererat.com', False)
print(contact2.list_contacts())
print(contact2.get_contact_by_id(2))
contact2.remove_contacts(2)
print(contact2.list_contacts())
