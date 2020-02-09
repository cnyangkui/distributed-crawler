# -*- encoding: utf-8 -*-

class Proxy(object):

    def __init__(self, ip, port, type):
        self.ip = ip
        self.port = port
        self.type = type

    def display(self):
        return "ip:"+self.ip+",port: "+self.port+",type:"+self.type