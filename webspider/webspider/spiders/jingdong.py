# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem
import re
import requests
import json
from lxml import etree

book_dict = {}


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['book.jd.com']
    start_urls = ['https://book.jd.com/booksort.html']
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

    def start_requests(self):
        global book_dict
        '调节数据为10000000～20000000全量爬取'
        for book_id in range(12115149,12115152):
            price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + str(book_id)
            briefing_url = 'https://dx.3.cn/desc/' + str(book_id)
            book_price = requests.get(url=price_url)
            book_briefing = requests.get(url=briefing_url)
            book_dict[str(book_id) + '_P'] = "无价格"
            book_dict[str(book_id) + '_B'] = '无简介'
            if book_price.status_code == 200:
                book_dict[str(book_id) + '_P'] = '¥' + json.loads(book_price.text)[0]['p']
            if book_briefing.status_code == 200:
                selector = etree.HTML(book_briefing.text)
                # 这里有问题，无法正确通过xpath获取简介内容，只能得到空列表。具体可以点开dx.3.cn那个网站看一下
                # 此外，有些书（例如id为35286025462的这一本），它的简介不在这个编号下，而是在12154359045下，这就很扯……
                book_dict[str(book_id) + '_B'] = \
                    str(selector.xpath("//*[@id='\"detail-tag-id-3\"']/div[2]/div/text()"))

            yield scrapy.Request('https://item.jd.com/{}.html'.format(book_id), self.parse)
    
    def parse(self, response):
        global book_dict
        book_id = response.url[20:-5]
        if response.css('.first > a::text').extract_first() == '图书':
            new_book = BookItem()
            new_book['title'] = response.css('.sku-name ::text').extract_first().strip()
            new_book['author'] = ' '.join(response.css('.p-author > a::attr(data-name)').extract())
            new_book['publisher'] = response.css('.p-parameter li::attr(title)').extract_first()
            new_book['publishDate'] = self.extract_date(response.css('.p-parameter li::attr(title)').extract())
            new_book['coverUrl'] = response.css('.main-img > img::attr(src)').extract_first()[2:]
            new_book['source'] = '京东网'
            # 因为动态加载的原因，无法获取下述两项
            new_book['price'] = book_dict[str(book_id) + '_P']
            del book_dict[str(book_id) + '_P']
            new_book['briefing'] = book_dict[str(book_id) + '_B']
            del book_dict[str(book_id) + '_B']
            yield new_book
    
    def extract_date(self, li):
        for i in li:
            if self.date_pattern.search(i):
                return i
        return None