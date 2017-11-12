# -*- encoding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
#import pymongo

class ExamplePipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name

        # '''数据插入taobao的数据库'''
        # conn = pymongo.MongoClient()
        # tbd = conn.youyuan
        # post_info = tbd.test
        # data = {'header_url': item["header_url"], 'pic_urls': item["pic_urls"], 'username': item["username"],
        #         'monologue': item["monologue"], 'age': item["age"], 'source': item["source"],
        #         'source_url': item["source_url"], 'crawled': item["crawled"], 'spider': item["spider"]}
        # post_info.insert(data)

        return item