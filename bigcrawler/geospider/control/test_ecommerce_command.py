#-*- encoding: utf-8 -*-
import redis
from copy import deepcopy
from scrapy import cmdline
import pymongo

from geospider.spiders.shop_keyword_spider import ShopKeywordSpider
from geospider.spiders.shop_main_spider import ShopMainSpider

client = pymongo.MongoClient('mongodb://localhost:27017')
db_name = 'geospider'
db = client[db_name]

def start():

    b = deepcopy(ShopKeywordSpider)
    b.name='aaa'
    b.keywords = ['手机']
    b.redis_key = "aaa:start_urls"
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # r.sadd("myspider:start_urls", 'http://news.qq.com/')
    r.lpush("aaa:start_urls", "https://www.taobao.com/")
    # r.lpush("aaa:start_urls", "http://news.sohu.com/")
    b.allowed_domains=["taobao.com"]
    cmdline.execute("scrapy crawl aaa".split())

    # process = CrawlerProcess(get_project_settings())
    # process.crawl(news_spider)
    # process.start()  # the script will block here until the crawling is finished

def pause():
    cmdline.execute("".split())

if __name__ == '__main__':
    start()

