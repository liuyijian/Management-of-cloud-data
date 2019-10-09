# -*- coding: utf-8 -*-
import scrapy


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['book.jd.com']
    start_urls = ['http://book.jd.com/']

    def parse(self, response):
        pass
