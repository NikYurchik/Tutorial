import configparser
from mongoengine import *
from mongoengine.fields import DateTimeField, ListField, StringField


config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('DB', 'user')
password = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

url = f"mongodb+srv://{username}:{password}@{domain}/{db_name}"

connect(host=url, ssl=True)


class Autor(Document):
    fullname = StringField(max_length=60, required=True, unique=True)
    born_date = DateTimeField()
    born_location = StringField(max_length=120)
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=40))
    quote = StringField(required=True)
    author = ReferenceField(Autor, reverse_delete_rule=CASCADE)
    meta = {'allow_inheritance': True}


