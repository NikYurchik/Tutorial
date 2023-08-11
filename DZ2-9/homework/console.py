import redis
from redis_lru import RedisLRU

from models import Autor, Quote
import crud

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def quote_read(author: Autor|str=None, tags: list|str=None):
    quote = crud.quote_read(author=author, tags=tags)
    return quote
    
@cache
def quote_find(author_mask: str=None, tags_mask: str=None):
    quote = crud.quote_find(author_mask=author_mask, tags_mask=tags_mask)
    return quote


def main():
    """
    Пошук цитат за ім'ям автора, за тегом або набором тегів.
    
    Формат - команда: значення
    Приклади:
        name: Steve Martin
        tag: humor
        tags: obvious, simile

    Значення для команд name та tag можна задавати частково або маскою з використанням символів:
        '^' - з початку строки;
        '$' - з кінця строки.
    Приклади:
        name: eve
        tag: ^hu
        tag: ous$
    """
    print("Скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів.\nФормат - команда: значення")
    while True:
        inp = input('>>> ')
        if inp == 'exit':
            print('До побачення.')
            break

        ls = inp.split(':')
        cmd = ls.pop(0)
        if cmd not in ['name', 'tag', 'tags']:
            print('Невідома команда!')
            continue
        if len(ls) == 0:
            print('Після : повинен бути параметр!')
            continue
        par = ls[0].strip()

        if cmd == 'name':
            quote = quote_read(author=par)
            if not quote:
                quote = quote_find(author_mask=par)
        elif cmd == 'tag':
            quote = quote_read(tags=par)
            if not quote:
                quote = quote_find(tags_mask=par)
        elif cmd == 'tags':
            ls = par.replace(' ','').split(',')
            quote = quote_read(tags=ls)
        
        if len(quote) == 0:
            print('Нічого не знайдено')
        else:
            n = 1
            for q2 in quote:
                print(str(n) + ': ' + q2.quote)
                n += 1

if __name__ == '__main__':
    main()

