from datetime import datetime, date
from bson.objectid import ObjectId

from dateutil.parser import *
from mongoengine import *

from models import Autor, Quote


def author_create(
        fullname: str, 
        born_date: str|datetime=None, 
        born_location: str=None, 
        description: str=None):
    """
    
    """
    if not fullname:
        raise ValueError('Author.fullname required!')
    bd = born_date if isinstance(born_date, date) else parse(born_date).date()
    author = Autor(fullname=fullname,
                    born_date=bd,
                    born_location=born_location, 
                    description=description).save()
    return author


def author_read(
        _id: str=None,
        fullname: str=None, 
        born_date: str|datetime=None, 
        born_location: str=None):

    if _id:
        author = Autor.objects(pk=ObjectId(_id))
    elif fullname:
        if born_date:
            bd = born_date if isinstance(born_date, date) else parse(born_date).date()
            if born_location:
                author = Autor.objects(
                            fullname=fullname,
                            born_date=bd,
                            born_location=born_location)
            else:
                author = Autor.objects(
                            fullname=fullname,
                            born_date=bd)
        else:
            if born_location:
                author = Autor.objects(
                            fullname=fullname,
                            born_location=born_location)
            else:
                author = Autor.objects(fullname=fullname)
    else:
        if born_date:
            bd = born_date if isinstance(born_date, date) else parse(born_date).date()
            if born_location:
                author = Autor.objects(
                            born_date=bd,
                            born_location=born_location)
            else:
                author = Autor.objects(born_date=bd)
        else:
            if born_location:
                    author = Autor.objects(born_location=born_location)
            else:
                    author = Autor.objects()
    return author


def author_find_by_mask(mask: str):
    author = Autor.objects(Q(fullname__regex=mask) | Q(born_location__regex=mask) | Q(description__regex=mask))
    return author


def author_find(fullname_mask: str=None, born_location_mask: str=None, description_mask: str=None):
    if fullname_mask:
        if born_location_mask:
            if description_mask:
                author = Autor.objects(fullname__regex=fullname_mask, born_location__regex=born_location_mask, description__regex=description_mask)
            else:
                author = Autor.objects(fullname__regex=fullname_mask, born_location__regex=born_location_mask)
        else:
            if description_mask:
                author = Autor.objects(fullname__regex=fullname_mask, description__regex=description_mask)
            else:
                author = Autor.objects(fullname__regex=fullname_mask)
    else:
        if born_location_mask:
            if description_mask:
                author = Autor.objects(born_location__regex=born_location_mask, description__regex=description_mask)
            else:
                author = Autor.objects(born_location__regex=born_location_mask)
        else:
            if description_mask:
                author = Autor.objects(description__regex=description_mask)
            else:
                author = Autor.objects()
    return author


def author_update(
        _id: str,
        fullname: str=None, 
        born_date: str|datetime=None, 
        born_location: str=None, 
        description: str=None):
    
    author = Autor.objects(pk=ObjectId(_id)).first()
    if author:
        fullname = fullname if not fullname is None else author.fullname
        if not born_date is None:
            born_date = born_date if isinstance(born_date, date) else parse(born_date).date()
        else:
            born_date = author.born_date
        born_location = born_location if not born_location is None else author.born_location
        description = description if not description is None else author.description
        author.update(
                    fullname=fullname,
                    born_date=born_date,
                    born_location=born_location, 
                    description=description)
        author.reload()
    else:
        author = author_create(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
    return author


def autor_delete(_id: str):
    author = Autor.objects(pk=ObjectId(_id))
    if author:
        author.first().delete()


def quote_create(author: Autor|str, quote: str, tags: list):
    if not isinstance(author, Autor):
        auth = author_read(fullname=author).first()
        author = auth if auth else author_create(fullname=author)
    quote = Quote(author=author, quote=quote, tags=tags).save()
    return quote


def quote_read(_id: str=None, author: Autor|str=None, quote: str=None, tags: list|str=None):
    if tags:
        tag = tags if isinstance(tags, list) else [tags]
    if _id:
        q1 = Quote.objects(pk=ObjectId(_id))
    elif author:
        if not isinstance(author, Autor):
            author = author_read(fullname=author)
            if author:
                author = author.first()
            else:
                return []
        if quote:
            if tags:
                q1 = Quote.objects(author=author, quote=quote, tags__in=tag)
            else:
                q1 = Quote.objects(author=author, quote=quote)
        else:
            if tags:
                q1 = Quote.objects(author=author, tags__in=tag)
            else:
                q1 = Quote.objects(author=author)
    else:
        if quote:
            if tags:
                q1 = Quote.objects(quote=quote, tags__in=tag)
            else:
                q1 = Quote.objects( quote=quote)
        else:
            if tags:
                q1 = Quote.objects(tags__in=tag)
            else:
                q1 = Quote.objects()
    return q1


def quote_find_by_mask(mask: str):
    auth = Autor.objects(fullname__regex=mask)
    if auth:
        a2 = []
        for a1 in auth:
            a2.append(a1.pk)

    quote = Quote.objects(Q(tags__regex=mask) | Q(quote__regex=mask) | Q(author__in=a2))
    return quote


def quote_find(author_mask: str=None, quote_mask: str=None, tags_mask: str=None):
    a2 = []
    if author_mask:
        auth = author_find(fullname_mask=author_mask)
        if auth:
            for a1 in auth:
                a2.append(a1.pk)
        else:
            return []
        
    if tags_mask:
        if quote_mask:
            if a2:
                quote = Quote.objects(tags__regex=tags_mask, quote__regex=quote_mask, author__in=a2)
            else:
                quote = Quote.objects(tags__regex=tags_mask, quote__regex=quote_mask)
        else:
            if a2:
                quote = Quote.objects(tags__regex=tags_mask, author__in=a2)
            else:
                quote = Quote.objects(tags__regex=tags_mask)
    else:
        if quote_mask:
            if a2:
                quote = Quote.objects(quote__regex=quote_mask, author__in=a2)
            else:
                quote = Quote.objects(quote__regex=quote_mask)
        else:
            if a2:
                quote = Quote.objects(author__in=a2)
            else:
                quote = Quote.objects()
    return quote


def quote_update(_id: str, author: Autor|str=None, quote: str=None, tags: list=None):
    quote1 = Quote.objects(pk=ObjectId(_id)).first()
    if quote1:
        if not isinstance(author, Autor):
            if not author:
                author = quote1.author
            else:
                auth = author_read(fullname=author)
                author = auth.first() if auth else author_create(fullname=author)
        quote = quote if not quote is None else quote1.quote
        tags = tags if not tags is None else quote1.tags
        quote1.update(author=author, quote=quote, tags=tags)
        quote1.reload()
    else:
        try:
            quote1 = quote_create(author=author, quote=quote, tags=tags)
        except ValueError as err:
            raise Exception(f'Quote "{_id}" not exists and {err}!')
    return quote1


def quote_delete(_id: str):
    quote = Quote.objects(pk=ObjectId(_id))
    if quote:
        quote.first().delete()


if __name__ == '__main__':
    qt = quote_read(tags="testc").first()
    tg = qt.tags
    tg.append('testu')
    qu = quote_update(_id=qt.id, quote=qt.quote+'/update', tags=tg)
    print(qu.id, qu.tags, qu.author.fullname, f'"{qu.quote}"')
