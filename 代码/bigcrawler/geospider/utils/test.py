# -*- encoding: utf-8 -*-
# -*- encoding: utf-8 -*-
import redis

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


if __name__ == '__main__':
    message = Message('127.0.0.1')
    message.subscribe('crawler')
    message.publish('crawler', 'op=stoptask&taskid=594be4f79c1da93dba43a3d6')
