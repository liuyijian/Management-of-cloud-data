# 以图搜书--检索系统
* 软件61 刘译键 2016013239

* 软件61 卢北辰 2016013242

## 前端

* 使用 vue + element



## 后端

* 使用 flask

* [pymongo 官方文档](https://api.mongodb.com/python/current/index.html)

## 爬虫

#####爬虫参考资料

* [豆瓣图书爬虫](https://github.com/40robber/ScrapyDouban)
* [当当图书爬虫](https://github.com/HunterChao/Dangdang/blob/master/Dangdang/dangdang/spiders/dangdang.py)
* [京东图书爬虫1](https://book.jd.com/booksort.html)
* [京东图书爬虫2](https://www.cnblogs.com/kangoroo/p/6071501.html)

* [爬虫IP代理池](https://scylla.wildcat.io/zh/latest/)

* [scrapy-css](<http://www.scrapyd.cn/doc/185.html>)

* [scrapy-xpath](http://www.scrapyd.cn/doc/186.html)

* [scrapy-splash](https://www.cnblogs.com/jclian91/p/8590617.html)

#####爬虫小范围测试debug

```python
# settings.py 中 请更换为本机mongodb配置信息
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USER = 'root'
MONGO_PASS = 'lyj271271'
MONGODB_DB_NAME = 'scrapy_data'
MONGODB_OVERWRITE_SIGN = True
```

```python
# pipelines.py 中 请注释掉以下代码，则不会写入mongodb
ITEM_PIPELINES = {
   'webspider.pipelines.MongoDBPipeline': 300,
}
```

```bash
# 命令行执行命令
cd webspider
scrapy crawl <spider-name> -o test.csv
```

##### 爬虫代理

* 使用docker安装代理池（运行后需要等待一段时间）

* ```bash
  docker run -d -p 8899:8899 -p 8081:8081 -v /var/www/scylla:/var/www/scylla --name scylla wildcat/scylla:latest
  ```

* 使用scylla的正向代理，爬虫程序中使用``http://127.0.0.1:8081``，则scylla会从代理池中选择一个代理进行爬取

##### 爬虫整合到restful api

* [scrapyrt](https://www.cnblogs.com/lxbmaomao/p/10372235.html)