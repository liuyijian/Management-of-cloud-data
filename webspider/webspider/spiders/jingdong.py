# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem
import re

class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['book.jd.com']
    start_urls = ['https://book.jd.com/booksort.html']
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

    def start_requests(self):
        '调节数据为10000000～20000000全量爬取'
        for book_id in range(12115149,12115152):
            yield scrapy.Request('https://item.jd.com/{}.html'.format(book_id), self.parse)
    
    def parse(self, response):
        if response.css('.first > a::text').extract_first() == '图书':
            new_book = BookItem()
            new_book['title'] = response.css('.sku-name ::text').extract_first().strip()
            new_book['author'] = ' '.join(response.css('.p-author > a::attr(data-name)').extract())
            new_book['publisher'] = response.css('.p-parameter li::attr(title)').extract_first()
            new_book['publishDate'] = self.extract_date(response.css('.p-parameter li::attr(title)').extract())
            new_book['coverUrl'] = response.css('.main-img > img::attr(src)').extract_first()[2:]
            new_book['source'] = '京东网'
            # 因为动态加载的原因，无法获取下述两项
            new_book['price'] = '无价格' or response.css('.p-price ::text').extract_first()
            new_book['briefing'] = '无简介' or response.css('.book-detail-content ::text').extract_first().strip()
            yield new_book
    
    def extract_date(self, li):
        for i in li:
            if self.date_pattern.search(i):
                return i
        return None