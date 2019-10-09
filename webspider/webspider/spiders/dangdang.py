# -*- coding: utf-8 -*-
import scrapy


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['book.dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        pass
