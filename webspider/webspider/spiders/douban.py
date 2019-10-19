# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/']
    
    def parse(self, response):
        for tag in response.css('.tagCol a::attr(href)').extract():
            for num in range(0,1000,20):
                yield scrapy.Request('https://book.douban.com' + tag + '?start=' + str(num), callback=self.parse_page)

    def parse_page(self, response):
        for item in response.css('.subject-item'):
            new_book = BookItem()
            new_book['title'] = item.css('.info a::attr(title)').extract_first()
            info_list = item.css('.pub ::text').extract_first().split('/')
            new_book['author'] = info_list[0].strip()
            new_book['publisher'] = info_list[-3].strip()
            # new_book['publishDate'] = info_list[-2].strip()
            # new_book['price'] = info_list[-1].strip()
            new_book['coverUrl'] = item.css('.pic img::attr(src)').extract_first()
            new_book['source'] = '豆瓣网'
            # new_book['briefing'] = item.css('p ::text').extract_first()
            yield new_book