import os
import pathlib
import json

import requests
from bs4 import BeautifulSoup


AUTHORS_FILE = 'data/authors.json'
QUOTES_FILE = 'data/quotes.json'

url = 'https://quotes.toscrape.com/'

def parse_quotes():
    store_ = []
    html_doc = requests.get(url)

    while True:
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            page = soup.select('div[class=row] > div[class=col-md-8]')[0]
            quotes = page.find_all('div', attrs={'class': 'quote'})
            for quote1 in quotes:
                quote = quote1.find('span', attrs={'class': 'text'}).text
                # quote = quote.replace('“', '').replace('”', '')
                author = quote1.find('small', attrs={'class': 'author'}).text
                autor_url = quote1.find_all('span')
                autor_url = autor_url[1].find('a')['href']
                tags1 = quote1.select('div[class=tags] > a[class=tag]')
                tags = []
                for tag in tags1:
                    tags.append(tag.text)

                store_.append({
                    'tags': tags,
                    'author': author,
                    'autor_url': autor_url,
                    'quote': quote
                })
    
            next = page.find('ul', attrs={'class': 'pager'}).find('li', attrs={'class': 'next'})
            if not next:
                break

            next = next.find('a')['href']
            next_url = f'{url}{next[1:]}'
            print(next_url)
            html_doc = requests.get(next_url)

    return store_


def parse_autor(quotes):
    authors = {}
    for quote in quotes:
        author = quote.get('author')
        a = authors.get(author)
        a_url = quote.pop('autor_url')
        if not a:
            authors.update({author: a_url})

    store_ = []
    for author, a_url in authors.items():
        a_url = f'{url}{a_url[1:]}'
        print(f'{author}: {a_url}')
        html_doc = requests.get(a_url)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            page = soup.select('div[class=author-details]')[0]
            borndate = page.find('span', attrs={'class': 'author-born-date'}).text
            bornplace = page.find('span', attrs={'class': 'author-born-location'}).text
            descr = page.find('div', attrs={'class': 'author-description'}).text
            store_.append({
                "fullname": author,
                "born_date": borndate,
                "born_location": bornplace,
                "description": descr.strip()
            })
    return store_


def main():
    """
    Скрапінг сайту https://quotes.toscrape.com з використанням BeautifulSoup.

    Обробляються всі сторінки сайту, в т.ч. сторінки з даними авторів цитат.
    У папці "data" формуються 2 файли:
        quotes.json - цитати;
        authors.json - дані авторів цитат.

    Запуск скрапінгу:
        py main.py
    або
        python3 main.py

    Отримані файли можна завантажити в базу даних MongoDB скриптом load.py
    Перевірити коректність скрапінгу та завантаження можна консольним скриптом console.py
    """
    quotes = parse_quotes()
    autors = parse_autor(quotes)


    file_path = pathlib.Path(os.path.dirname(AUTHORS_FILE))
    if not file_path.exists():
        file_path.mkdir(parents=True)
    with open(AUTHORS_FILE, 'w', encoding='utf-8') as file:
        json.dump(autors, file, ensure_ascii=False, indent=2)

    file_path = pathlib.Path(os.path.dirname(QUOTES_FILE))
    if not file_path.exists():
        file_path.mkdir(parents=True)
    with open(QUOTES_FILE, 'w', encoding='utf-8') as file:
        json.dump(quotes, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
