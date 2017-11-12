# -*- encoding: utf-8 -*-
import os

from copy import deepcopy

import time

import signal

import sys
from scrapy import cmdline

from geospider.ecommerce.spiderUtils.url_utils import get_domain
from geospider.spiders.blog_spider import BlogSpider
from geospider.spiders.blog_spider_recover import BlogSpiderRecover
from geospider.spiders.news_spider import NewsSpider
from geospider.spiders.news_spider_recover import NewsSpiderRecover
from geospider.spiders.shop_keyword_spider import ShopKeywordSpider
from geospider.spiders.shop_main_spider import ShopMainSpider
from geospider.utils.mongodb_helper import connect_mongodb, TaskDao, ProcessDao
from geospider.utils.redis_helper import connect_redis, URLDao
from geospider.utils.settings_helper import get_attr
from geospider.utils.time_util import compare_time


def init(taskid, is_restart):
    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    task = taskdao.find_by_id(taskid)
    temp = None
    if "news" == task['webtype']:
        if is_restart:
            temp = deepcopy(NewsSpiderRecover)
        else:
            temp = deepcopy(NewsSpider)
    elif "blog" == task['webtype']:
        if is_restart:
            temp = deepcopy(BlogSpiderRecover)
        else:
            temp = deepcopy(BlogSpider)
    elif "ecommerce" == task['webtype']:
        keywords = task['keywords']
        if len(keywords)==0:
            temp = deepcopy(ShopMainSpider)
        else:
            temp = deepcopy(ShopKeywordSpider)
            temp.keywords = keywords
    temp.name = taskid
    temp.redis_key = taskid + ":start_urls"


    redis = connect_redis()
    url_manager = URLDao(redis)
    allowed_domains = []
    if task['webtype']=='news' or task['webtype']=='blog':
        for url in task['starturls']:
            url_manager.insert_url(taskid, url)
            print(get_domain(url))
            allowed_domains.append(get_domain(url))
        temp.allowed_domains = allowed_domains
    elif task['webtype']=='ecommerce':
        for url in task['starturls']:
            url_manager.insert_url(taskid, url)


def run(taskid):
    # sys.path.append('/opt/graphite/webapp/')
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphite.local_settings")
    cmdline.execute(("scrapy crawl " + taskid).split())


def wait(taskid):
    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    task = taskdao.find_by_id(taskid)

    starttime = task['starttime']
    endtime = task['endtime']
    localhost = get_attr('LOCAL_HOST')
    flag = False
    while (flag is False):
        flag = compare_time(time.strftime("%Y/%m/%d %H:%M"), starttime, endtime)
        time.sleep(30)
    if flag is True:
        task['status'] = 'running'
        taskdao.save(task)
        processdao = ProcessDao(mongodb)
        processdao.update_status_by_localhost_and_taskid(localhost, taskid, 'running')
        run(taskid)


def delete(taskid, is_changed):
    redis = connect_redis()
    url_manager = URLDao(redis)
    url_manager.delete_task(taskid)

    if is_changed:
        mongodb = connect_mongodb()
        taskdao = TaskDao(mongodb)
        task = taskdao.find_by_id(taskid)

        endtime = time.strftime("%Y/%m/%d %H:%M")
        task['endtime'] = endtime
        taskdao.save(task)


def scaner():
    mongodb = connect_mongodb()
    taskdao = TaskDao(mongodb)
    processdao = ProcessDao(mongodb)
    localhost = get_attr('LOCAL_HOST')
    print(localhost)
    while (True):
        task_list = taskdao.find_by_localhost_and_status(localhost, 'running')
        for t in task_list:
            starttime = t['starttime']
            endtime = t['endtime']
            print(starttime + " " + endtime)
            if endtime != '':
                if compare_time(time.strftime("%Y/%m/%d %H:%M"), starttime, endtime) is False:
                    taskid = str(t['_id'])
                    print(taskid)
                    process_list = processdao.find_by_localhost_and_taskid(localhost, taskid)
                    for p in process_list:
                        if p['taskid'] == taskid and p['status'] != 'stopping':
                            print("杀死进程%s" % (p['pid']))
                            # p.terminate()
                            try:
                                os.kill(p['pid'], signal.SIGKILL)
                            except:
                                continue
                    delete(taskid, False)
                    t['status'] = 'stopping'
                    taskdao.save(t)
                    processdao.delete_by_localhost_and_taskid(localhost, taskid)
        time.sleep(30)
