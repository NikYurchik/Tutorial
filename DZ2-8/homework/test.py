from bson.objectid import ObjectId

from mongoengine import *

from models import Autor, Quote


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


if __name__ == '__main__':
    # q1 = Quote.objects(pk=ObjectId("64cad4a17eb56a00d573125a")).first()
    # q1 = Quote.objects(tags__regex='ous$')
    # print(q1)
    # for qu in q1:
    #     print(qu.id, qu.tags, qu.author.fullname, f'"{qu.quote}"')

    a2 = author_find('^Steve')
    for qu in a2:
        print(qu.id, qu.fullname, qu.born_date, f'"{qu.born_location}"')

    q2 = quote_find(tags_mask='ous$')
    for qu in q2:
        print(qu.id, qu.tags, qu.author.fullname, f'"{qu.quote}"')
