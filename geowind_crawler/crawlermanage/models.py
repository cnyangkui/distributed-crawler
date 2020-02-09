import datetime

import mongoengine
from mongoengine import Document, StringField, ListField

# Create your models here.

class User(Document):
    username = StringField(max_length=30, required=True)
    password = StringField(max_length=30, required=True)

class Task(Document):
    taskname = StringField(max_length=30, required=True)
    starturls = ListField(required=True)
    starttime = StringField(max_length=20, required=True, editable=False)
    endtime = StringField(max_length=20)
    webtype = StringField(max_length=20)
    describe = StringField(max_length=100)
    slave = ListField(required=True)
    status = StringField(max_length=10)
    processnum = mongoengine.IntField()
    keywords = ListField()

class News(Document):
    title = StringField(max_length=30, required=True)
    url = StringField(max_length=200, required=True)
    article = StringField(max_length=2000)
    time = StringField(max_length=20)
    keywords = StringField(max_length=30)
    taskid = StringField(max_length=30, required=True)

class Blog(Document):
    title = StringField(max_length=30, required=True)
    url = StringField(max_length=200, required=True)
    article = StringField(max_length=2000)
    time = StringField(max_length=20)
    keywords = StringField(max_length=30)
    taskid = StringField(max_length=30, required=True)

class Process(Document):
    localhost = StringField(max_length=30, required=True)
    pid = StringField(max_length=30, required=True)
    taskid = StringField(max_length=30, required=True)
    status = StringField(max_length=30, required=True)

class Machine(Document):
    ip = StringField(max_length=30, required=True)


class Goods(Document):
    title = StringField(max_length=100,required=True)
    price = StringField(max_length=100,required=True)
    pic_url = StringField(max_length=100,required=True)
    detail_url = StringField(max_length=100,required=True)
    comments_number = StringField(max_length=10,required=True)
    comment_degree = StringField(max_length=100,required=True)
    comments = ListField()
    description = StringField(max_length=200,required=True)
    taskid = StringField(max_length=30, required=True)

class Stores(Document):
    name = StringField(max_length=100,required=True)
    store_url = StringField(max_length=100,required=True)
    description = StringField(max_length=300,required=True)
    comment_degree = StringField(max_length=10, required=True)
    taskid = StringField(max_length=30, required=True)

class TempArticle(Document):
    url = StringField(max_length=200, required=True)
    title = StringField(max_length=100)
    time = StringField(max_length=20)
    keywords = StringField(max_length=100)
    article = StringField(max_length=50000)

class TempGoods(Document):
    title = StringField(max_length=200, required=True)
    price = StringField(max_length=100, required=True)
    pic_url = StringField(max_length=500, required=True)
    detail_url = StringField(max_length=500, required=True)
    comment_degree = StringField(max_length=20000, required=True)

class Proxy(Document):
    proxy = StringField(max_length=5000)
    status = StringField(max_length=2)

class Prewebsite(Document):
    url = StringField(max_length=5000)
    name = StringField(max_length=1000)
    webtype = StringField(max_length=500)
