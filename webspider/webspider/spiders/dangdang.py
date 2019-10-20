# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem
import itertools


def generate_page_url(url):
        # 全量爬将5改成100
        li = [url[:29] + 'pg' + str(i) + '-' + url[29:] for i in range(1,100)]
        li.append(url)
        return li

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # 全量爬将5改成100
    li = [str(i).zfill(2) for i in range(100)]
    urls_with_type = list(map(lambda x: 'http://category.dangdang.com/cp01.{}.00.00.00.00.html'.format(x), li))
    urls_with_type_with_page = sum(list(map(generate_page_url,urls_with_type)),[])
    start_urls = urls_with_type_with_page 

    def parse(self, response):
        for i in response.css('#component_59 > li'):
            new_book = BookItem()
            new_book['title'] = i.css('.name > a::attr(title)').extract_first()
            new_book['coverUrl'] = i.css('.pic > img::attr(data-original)').extract_first() or i.css('.pic > img::attr(src)').extract_first()
            # new_book['briefing'] = i.css('.detail ::text').extract_first()
            # new_book['price'] = i.css('.price > .search_now_price ::text').extract_first()
            new_book['author'] = i.css('.search_book_author > span:nth-child(1) > a ::text').extract_first()
            # new_book['publishDate'] = i.css('.search_book_author > span:nth-child(2) ::text').extract_first()
            new_book['publisher'] = i.css('.search_book_author > span:nth-child(3) > a ::text').extract_first()
            new_book['source'] = '当当网'
            yield new_book

    