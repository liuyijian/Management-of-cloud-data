# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem
import re
import requests
import json


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['book.jd.com']
    start_urls = ['https://book.jd.com/booksort.html']
    price_url_prefix = 'https://p.3.cn/prices/mgets?skuIds=J_'
    briefing_url_prefix = 'https://dx.3.cn/desc/'
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    tag_pattern = re.compile('<[^>]+>', re.S)

    def start_requests(self):
        '调节数据为10000000～20000000全量爬取'
        for book_id in range(10000000,20000000):
            print(book_id / 10000000 - 1)
            yield scrapy.Request('https://item.jd.com/{}.html'.format(book_id), self.parse)
    
    def parse(self, response):
        book_id = response.url[20:-5]
        if response.css('.first > a::text').extract_first() == '图书':
            new_book = BookItem()
            new_book['title'] = response.css('.sku-name ::text').extract_first().strip()
            new_book['author'] = ' '.join(response.css('.p-author > a::attr(data-name)').extract())
            new_book['publisher'] = response.css('.p-parameter li::attr(title)').extract_first()
            new_book['publishDate'] = self.extract_date(response.css('.p-parameter li::attr(title)').extract())
            new_book['coverUrl'] = response.css('.main-img > img::attr(src)').extract_first()[2:]
            new_book['source'] = '京东网'
            new_book['price'] = self.get_price(book_id)
            new_book['briefing'] = self.get_briefing(book_id)
            yield new_book
    
    def extract_date(self, li):
        for i in li:
            if self.date_pattern.search(i):
                return i
        return None

    def get_briefing(self,book_id):
        response = requests.get(url=self.briefing_url_prefix+book_id)
        if response.status_code == 200:
            s = response.text
            pos1 = s.find('book-detail-content')
            pos2 = s.find('</div>',pos1)
            return self.tag_pattern.sub('',''.join(s[pos1+23:pos2].strip().split()))
        else:
            return '无简介'

    def get_price(self,book_id):
        response = requests.get(url=self.price_url_prefix+book_id)
        if response.status_code == 200:
            return '¥' + json.loads(response.text)[0]['p']
        else:
            return '无价格'