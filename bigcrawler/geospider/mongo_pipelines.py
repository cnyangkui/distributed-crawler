# -*- encoding: utf-8 -*-
import pymongo

class MongoPipeline(object):

    collection_name = 't_news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print(dict(item))
        self.db[self.collection_name].insert(dict(item))
        # data = {'title': item["title"][0], 'link': item["link"], 'price': item["price"][0],
        #        'comment': item["comment"][0]}
        #data = {'title': item["title"], 'time': item["time"], 'keywords': item["keywords"],
        #        'acticle': item["acticle"]}
        #print data
        #self.db.insert(data)
        return item


# class TaobaoPipeline(object):
#     # def connect(self):
#     #     '''连接数据库'''
#     #     host = "localhost"
#     #     dbName = "taobao"
#     #     user = "root"
#     #     password = "123456"
#     #     db = pymysql.connect(host, user, password, dbName, charset='utf8')
#     #     return db   # 一定要返回连接的db
#     #     cursorDB = db.cursor()
#     #     return cursorDB
#
#     # def mysqlOpe(self):
#     #     sql = "insert into taobao(title,link,price,comment)VALUES(%s,%s,%s,%s)"
#     #     conn=self.connect()
#     #     cur = conn.cursor()
#     #     cur.execute(sql, (item["title"][0], item["link"], item["price"][0], item["comment"][0]))
#     #     conn.commit()
#     #     cur.close()
#
#     def process_item(self, item, spider):
#         '''数据插入taobao的数据库'''
#         conn = pymongo.MongoClient()
#         tbd = conn.Taobao
#         post_info = tbd.test2
#         data = {'title':item["title"][0],'link':item["link"],'price':item["price"][0],'comment':item["comment"][0]}
#         post_info.insert(data)
#         return item