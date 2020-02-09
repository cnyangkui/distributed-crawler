#-*- coding:utf-8 -*-
SPIDER_MODULES = ['geospider.spiders']
NEWSPIDER_MODULE = 'geospider.spiders'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#数据库设置
ITEM_PIPELINES = {
    #'spiderController.pipelines.ExamplePipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
    'geospider.mongodb_pipelines.MongoDBPipeline': 400,
}

#中间件设置，IP和浏览器代理
DOWNLOADER_MIDDLEWARES = {
    'geospider.middlewares.RotateUserAgentMiddleware':123,
    'geospider.middlewares.ProxyMiddleWare':124,
}
#相关IP设置，包括数据库，状态监控等等
REDIS_HOST = '192.168.1.105'
REDIS_PORT = 6379
SUBSCRIBE = 'crawler'
LOCAL_HOST = '192.168.1.105'
# STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'
STATS_CLASS = 'geospider.statscol.graphite.RedisGraphiteStatsCollector'
GRAPHITE_HOST = '123.207.230.48'
GRAPHITE_PORT = 2003
MONGO_URI = 'mongodb://192.168.1.105/'
MONGO_DATABASE = 'geospider'
MONGO_COLLECTION = 'news'
ROBOTSTXT_OBEY = False

#是否禁止cookies
COOKIES_ENABLED = False

LOG_LEVEL= 'DEBUG'

#除去一些没必要的日志输出
import logging
logging.getLogger('cluster.matrix').setLevel(logging.WARNING)
logging.getLogger('chardet.charsetprober').setLevel(logging.ERROR)


# import logging
# from scrapy.utils.log import configure_logging
#
# configure_logging(install_root_handler=False)
# logging.basicConfig(
#     filename='log.txt',
#     filemode = 'a',
#     format='%(levelname)s: %(message)s',
#     level=logging.DEBUG
# )
