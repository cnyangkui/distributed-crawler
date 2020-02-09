# -*- encoding: utf-8 -*-
import json

import mongoengine

from crawlermanage.models import Task, Process, Machine
from crawlermanage.utils.time_util import in_latest_weekend, get_weekday

'''
    创建当前任务状态表，返回4个数组
    运行[新闻，博客，电商]
    暂停[...]
    等待[...]
    故障[...]
'''

mongoengine.register_connection('default', 'geospider')


def create_chart1():
    run_news = Task.objects.filter(webtype='news', status='running').count()
    run_blog = Task.objects.filter(webtype='blog', status='running').count()
    run_ecommerce = Task.objects.filter(webtype='ecommerce', status='running').count()
    pause_new = Task.objects.filter(webtype='news', status='pausing').count()
    pause_blog = Task.objects.filter(webtype='blog', status='pausing').count()
    pause_ecommerce = Task.objects.filter(webtype='ecommerce', status='pausing').count()
    wait_news = Task.objects.filter(webtype='news', status='waitting').count()
    wait_blog = Task.objects.filter(webtype='blog', status='waitting').count()
    wait_ecommerce = Task.objects.filter(webtype='ecommerce', status='waitting').count()
    error_news = Task.objects.filter(webtype='news', status='error').count()
    error_blog = Task.objects.filter(webtype='blog', status='error').count()
    error_ecommerce = Task.objects.filter(webtype='ecommerce', status='error').count()
    run = [run_news, run_blog, run_ecommerce]
    pause = [pause_new, pause_blog, pause_ecommerce]
    wait = [wait_news, wait_blog, wait_ecommerce]
    error = [error_news, error_blog, error_ecommerce]
    return run, pause, wait, error


'''
    历史任务：各类型爬虫任务所占比例
    return：停止的电商任务个数，停止的新闻任务个数，停止的博客任务个数
'''


def create_chart2():
    ecommerce = Task.objects.filter(webtype='ecommerce', status='stopping').count()
    news = Task.objects.filter(webtype='news', status='stopping').count()
    blog = Task.objects.filter(webtype='blog', status='stopping').count()
    return ecommerce, news, blog

'''最近一周各类型任务数量统计'''
def create_chart3():
    ecommerce_tasks = Task.objects.filter(webtype='ecommerce')
    news_tasks = Task.objects.filter(webtype='news')
    blog_tasks = Task.objects.filter(webtype='blog')
    ecommerce_num = [0, 0, 0, 0, 0, 0, 0]
    news_num = [0, 0, 0, 0, 0, 0, 0]
    blog_num = [0, 0, 0, 0, 0, 0, 0]
    for t in ecommerce_tasks:
        taskdate = t['starttime']
        taskdate = taskdate.split(' ')[0]
        if in_latest_weekend(taskdate):
            index = get_weekday(taskdate)
            ecommerce_num[index] += 1
    for t in news_tasks:
        taskdate = t['starttime']
        taskdate = taskdate.split(' ')[0]
        if in_latest_weekend(taskdate):
            index = get_weekday(taskdate)
            news_num[index] += 1
    for t in blog_tasks:
        taskdate = t['starttime']
        taskdate = taskdate.split(' ')[0]
        if in_latest_weekend(taskdate):
            index = get_weekday(taskdate)
            blog_num[index] += 1
    return ecommerce_num, news_num, blog_num

'''每台主机运行的任务进程数量雷达图'''
def create_chart4():
    machine_list = Machine.objects.all()
    ip_list = []
    process_num = []
    for m in machine_list:
        ip = m['ip']
        data = "{name:'%s', max:%d}"%(ip, 30)
        ip_list.append(str(data))
        num = Process.objects.filter(localhost=ip).count()
        process_num.append(num)
    return ip_list, process_num




if __name__ == '__main__':
    print(create_chart4())
