import os
import pathlib
import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


AUTHORS_FILE = 'data/authors.json'
QUOTES_FILE = 'data/quotes.json'

url = 'https://quotes.toscrape.com/'


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append({
                "fullname": adapter["fullname"],
                "born_date": adapter["born_date"],
                "born_location": adapter["born_location"],
                "description": adapter["description"],
            })
        if 'quote' in adapter.keys():
            self.quotes.append({
                "tags": adapter["tags"],
                "author": adapter["author"],
                "quote": adapter["quote"],
            })
        return

    def close_spider(self, spider):
        file_path = pathlib.Path(os.path.dirname(QUOTES_FILE))
        if not file_path.exists():
            file_path.mkdir(parents=True)
        with open(QUOTES_FILE, 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)

        file_path = pathlib.Path(os.path.dirname(AUTHORS_FILE))
        if not file_path.exists():
            file_path.mkdir(parents=True)
        with open(AUTHORS_FILE, 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)


class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [url]
    custom_settings = {"ITEM_PIPELINES": {QuotesPipline: 300}}

    def parse(self, response, *args):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q1 = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=q1)
            a_url = self.start_urls[0] + quote.xpath('span/a/@href').get()[1:]
            yield response.follow(url=a_url, callback=self.nested_parse_author, cb_kwargs=dict(author_orig=author))

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response, author_orig, *args):
        author = response.xpath('/html//div[@class="author-details"]')
        fullname = author.xpath('h3[@class="author-title"]/text()').get().strip()
        fullname = author_orig.strip()
        born_date = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        description = author.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)


def main():
    """
    Скрапінг сайту http://quotes.toscrape.com з використанням фреймворку Scrapy.

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
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()


if __name__ == '__main__':
    main()
