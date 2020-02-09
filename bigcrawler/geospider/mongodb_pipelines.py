import pymongo
import logging

from copy import deepcopy
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.settings import Settings
from geospider.items import Goods, Stores, Ecommerce, News, Blog


class MongoDBPipeline(object):
    def __init__(self):
        self.url = settings['MONGO_URI']
        self.db = settings['MONGO_DATABASE']
        self.col = settings['MONGO_COLLECTION']


    def process_item(self, item, spider):
        # print("++++++++++++++++++++++++++++++++")
        classname = str(type(spider))
        # print(classname)

        myitem = deepcopy(item)
        url_key = 'url'
        if isinstance(item, News):
            self.col='news'
        elif isinstance(item, Blog):
            self.col='blog'
        elif isinstance(item,Ecommerce):
            print('******************ecommerce*****************************')
            myitem = item['goods']
            self.col = 'goods'
            url_key = 'detail_url'


            connection = pymongo.MongoClient(self.url)
            db = connection[self.db]
            self.collection = db[self.col]
            err_msg = ''
            for field, data in myitem.items():
                if not data:
                    err_msg += 'Missing %s of poem from %s\n' % (field, myitem[url_key])
            if err_msg:
                raise DropItem(err_msg)
            self.collection.insert(dict(myitem))
            logging.debug('Item written to MongoDB database %s/%s' % (self.db, self.col))

            self.col = 'stores'
            myitem = item['stores']
            url_key = 'store_url'



        connection = pymongo.MongoClient(self.url)
        db = connection[self.db]
        self.collection = db[self.col]
        err_msg = ''
        for field, data in myitem.items():
            if not data:
                err_msg += 'Missing %s of poem from %s\n' % (field, myitem[url_key])
        if err_msg:
            raise DropItem(err_msg)
        self.collection.insert(dict(myitem))
        logging.debug('Item written to MongoDB database %s/%s' % (self.db, self.col))
        return item