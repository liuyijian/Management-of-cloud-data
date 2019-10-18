from scrapy.item import Item
from scrapy.exceptions import DropItem
from functools import reduce
import re
import pymongo


class FormatterPipeline(object):
    '检查空属性；修正书名，日期，价格; 去重'
    def __init__(self):
        self.book_set = set()
        self.brackets_pattern = re.compile(u"\\(.*?\\)|\\{.*?}|\\[.*?]|\\（.*?）|\\「.*?」|\\【.*?】")
        self.date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    
    def process_item(self, item, spider):
        
        if not reduce(lambda x,y: x and y, item.values()):
            raise DropItem('存在空属性')
        
        if item['source'] == '京东网' and item['price'].startswith('-'):
            raise DropItem('无价格信息')

        if item['source'] == '当当网':
            item['title'] = self.brackets_pattern.sub('', item['title'].strip().split(' ')[0])
            pos1 = item['title'].find('(')
            if pos1 != -1:
                item['title'] = item['title'][:pos1]
            pos2 = item['title'].find('（')
            if pos2 != -1:
                item['title'] = item['title'][:pos2] 
            item['publishDate'] = self.date_pattern.search(item['publishDate']).group()

        digest = item['title'] + item['author'] + item['publisher'] + item['source']

        if digest in self.book_set:
            raise DropItem('重复书籍')
        else:
            self.book_set.add(digest)

        return item


class MongoDBPipeline(object):
    '存储进mongodb的管道,数据库名为scrapy_data,集合名为爬虫名'
    # 暂时的理解是item对应数据库中的一张表，而一个爬虫可以根据需要，将爬取的字段分表存储，而爬虫对应的pipeline也应该根据表的不同而做相应不同的处理
    def open_spider(self, spider):

        host = spider.settings.get('MONGO_HOST', 'localhost')
        port = spider.settings.get('MONGO_PORT', 27017)
        username = spider.settings.get('MONGO_USER', 'root')
        password = spider.settings.get('MONGO_PASS', 'root')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scrapy_data')        
        overwrite_sign = spider.settings.get('MONGODB_OVERWRITE_SIGN', False)
    
        # self.client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.collection = self.db[spider.name]

        # 若集合已存在且可覆盖标志设定为True，则覆盖之，对其他数据库管道也应该执行此项检查
        if self.collection.name in self.db.collection_names() and overwrite_sign:
            self.collection.drop()

    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        # 此处一个爬虫只对应一个item，若对应多个item，则应该根据item的类名来进行分类处理
        self.insert_db(item)
        return item
    
    def insert_db(self, item):
        post = dict(item) if isinstance(item, Item) else item
        self.collection.insert_one(post)
