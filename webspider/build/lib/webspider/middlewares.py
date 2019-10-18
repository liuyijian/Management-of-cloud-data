# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import json
import random


class RandomUserAgentMiddleware(object):
    '随机user-agent中间件'
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User_Agent',get_ua())

class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    '随机IP代理中间件'
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://127.0.0.1:8081'