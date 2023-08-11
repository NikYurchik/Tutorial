import json

from dateutil.parser import *
from mongoengine import *

from crud import author_create, quote_create, autor_drop, quote_drop

def load_json(filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_data():
    quote_drop()
    autor_drop()
    
    a_list = {}
    authors = load_json('data/authors.json')
    for auth in authors:
        fn = auth.get("fullname")
        sbd = auth.get("born_date")
        bd = parse(sbd).date()
        author = author_create(fn, bd, auth.get("born_location"), auth.get("description"))
        a_list.update({fn: author})
    
    quotes = load_json('data/quotes.json')
    for quot in quotes:
        auth = a_list.get(quot.get("author"))
        if not auth:
            auth = author_create(fn)
        quote = quote_create(auth, quot.get("quote"), quot.get("tags"))


if __name__ == '__main__':
    load_data()
