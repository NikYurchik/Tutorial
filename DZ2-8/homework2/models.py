import configparser
from mongoengine import *
from mongoengine.fields import StringField, EmailField, BooleanField


config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('DB', 'user')
password = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

url = f"mongodb+srv://{username}:{password}@{domain}/{db_name}"

connect(host=url, ssl=True)


class Contact(Document):
    fullname = StringField(max_length=60, required=True, unique=True)
    email = EmailField(max_length=60)
    is_email = BooleanField()
    phone = StringField(max_length=30)
    is_phone = BooleanField()
    is_send = BooleanField()

    def __init__(self, fullname: str, email: str, is_email: bool, phone: str, is_phone: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fullname = fullname
        self.email = email
        self.is_email = True if email and is_email else False
        self.phone = phone
        self.is_phone = True if phone and is_phone else False
        self.is_send = True
