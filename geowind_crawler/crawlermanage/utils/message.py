# -*- encoding: utf-8 -*-
import redis
from geowind_crawler import settings

'''
    消息发送订阅
    author:yangkui
'''
class Message(object):

    channels = []

    def __init__(self, host):
        self.host = host
        self.rc = redis.Redis(host=host)
        self.ps = self.rc.pubsub()

    def subscribe(self, channel):
        self.channels.append(channel)
        self.ps.subscribe(channel)

    def publish(self, subscriber, message):
        self.rc.publish(subscriber, message)

    def listen(self):
        for item in self.ps.listen():
            if item['type'] == 'message':
                return item['data']

if __name__ == '__main__':
    # message = Message('127.0.0.1')
    # message.subscribe('crawler')
    # message.subscribe('aaa')
    # message.publish('crawler', 'op=stoptask&taskid=592ceac49c1da96d222995d9')
    messager = Message('127.0.0.1')
    messager.subscribe('crawler')
    msg = 'is_start'
    messager.publish('crawler', msg)
    receive = messager.listen()
    print (receive)


    # redis_host=settings.__getattribute__('REDIS_HOST')
    # print(type(redis_host))