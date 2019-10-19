# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    # publishDate = scrapy.Field()
    # briefing = scrapy.Field()
    # price = scrapy.Field()
    coverUrl = scrapy.Field()
    source = scrapy.Field()

