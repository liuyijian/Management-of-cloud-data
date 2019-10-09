from scrapy.item import Item
import pymongo

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
    
        self.client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
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
