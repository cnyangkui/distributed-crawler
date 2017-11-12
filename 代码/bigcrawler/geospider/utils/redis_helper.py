# -*- encoding: utf-8 -*-
import redis

from geospider.utils.settings_helper import get_attr


def connect_redis():
    host = get_attr('REDIS_HOST')
    port = get_attr('REDIS_PORT')
    r = redis.Redis(host=host, port=port, db=0)
    return r


class URLDao(object):
    def __init__(self, redis):
        self.redis = redis

    def delete_task(self, taskid):
        self.redis.delete(taskid + ":requests")
        self.redis.delete(taskid + ":start_urls")
        self.redis.delete(taskid + ":dupefilter")

    def insert_url(self, taskid, url):
        self.redis.lpush(taskid + ":start_urls", url)
