# -*- encoding: utf-8 -*-
import csv

import mongoengine

# Create your tests here.
import sys

from crawlermanage.models import Task

reload(sys)
sys.setdefaultencoding('utf-8')
mongoengine.register_connection('default', 'geospider')


if __name__ == '__main__':
    list = Task.objects.all()
    for i in list:
        print(list['id'])