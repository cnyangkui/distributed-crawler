#-*- encoding: utf-8 -*-

class Analyze(object):

    dict = None

    def __init__(self, msg):
        self.dict = {}
        self.msg = msg
        params = self.msg.split('&')
        for p in params:
            key, value = p.split('=')[0], p.split('=')[1]
            self.dict[key] = value

    def dict(self):
        return self.dict

    def get(self, op):
        return self.dict.get(op)


if __name__ == '__main__':
    a = Analyze('d=e&u=d')
    dict = a.dict
    print(dict.get('e'))