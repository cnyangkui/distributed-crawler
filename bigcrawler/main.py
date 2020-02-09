# -*- encoding: utf-8 -*-
# import redis

# activate_this = '/home/kui/work/python/env/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
from geospider.spiders.news_spider import NewsSpider
#
# r = redis.Redis(host='127.0.0.1', port=6379, db=0)
# r.lpush('news:start_urls', 'http://news.qq.cn/')   #添加
# cmdline.execute("scrapy crawl news".split())


# redis-cli lpush myspider:start_urls http://google.com

from scrapy import cmdline
cmdline.execute("scrapy crawl shoptestspider".split())

