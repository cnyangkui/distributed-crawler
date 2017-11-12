# -*- encoding: utf-8 -*-
import os

import redis


class Messager(object):
    channels = []

    def __init__(self, host):
        self.rc = redis.Redis(host=host)
        self.ps = self.rc.pubsub()

    def subscribe(self, channel):
        self.channels.append(channel)
        self.ps.subscribe(channel)

    def listen(self):
        for item in self.ps.listen():
            if item['type'] == 'message':
                return item['data']

    def publish(self, subscriber, message):
        self.rc.publish(subscriber, message)


# if __name__ == '__main__':
#     listener = Messager('127.0.0.1')
#     listener.subscribe('crawler')
#     msg = listener.listen()
#     print(msg)
#     if msg =='is_start':
#         listener.publish('crawler', 'master:is_start')
