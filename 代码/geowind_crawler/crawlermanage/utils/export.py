# -*- encoding: utf-8 -*-
import os

import xlwt

from crawlermanage.models import News, Blog, Goods, Stores, Task


def news_and_blog_export(res_taskid,is_news):
    if(is_news == 'news'):
        newslist = News.objects.filter(taskid=res_taskid)
    else:
        newslist = Blog.objects.filter(taskid=res_taskid)

    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wbook = xlwt.Workbook()
    wsheet = wbook.add_sheet('export data')

    # logger.info(newslist)
    # logger.info(type(newslist))
    col = 1
    for each in newslist:
        row = 0

        each_dic = []
        each_dic.append(each['title'])
        each_dic.append(each['url'])
        each_dic.append(each['time'])
        each_dic.append(each['keywords'])
        each_dic.append(each['article'])

        for k in each_dic:
            wsheet.write(col, row, k)
            row += 1
        col += 1

    task_message = Task.objects.filter(id=res_taskid).get(0)
    title = task_message['taskname'] + '(' + ','.join(list(task_message['starturls'])) + ')'

    base_dir = os.path.dirname(os.path.abspath(__file__))

    filepath = base_dir + '/media/dataexport/' + res_taskid + '.xls'

    if (os.path.exists(filepath)):
        os.remove(filepath)

    wbook.save(filepath)
    return filepath
def ecommerce_export(res_taskid):
    res_taskid = '5960a659c5d5860f15e6d470'


    goodslist = Goods.objects.filter(taskid=res_taskid)
    storeslist = Stores.objects.filter(taskid=res_taskid)

    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wbook = xlwt.Workbook()
    goods_sheet = wbook.add_sheet('goods')
    stores_sheet = wbook.add_sheet('stores')

    task_message = Task.objects.filter(id=res_taskid).get(0)
    title = task_message['taskname'] + '(' + ','.join(list(task_message['starturls'])) + ')'



    col = 1
    for each in goodslist:
        row = 0
        each_dic = []
        each_dic.append(each['title'])
        each_dic.append(each['price'])
        each_dic.append(each['detail_url'])
        each_dic.append(each['comment_degree'])
        each_dic.append(each['pic_url'])

        for k in each_dic:
            goods_sheet.write(col, row, k)
            row += 1
        col += 1
    goods_sheet.write_merge(0, 0, 0, 4, title)

    col = 1
    for each in storeslist:
        row = 0
        each_dic = []
        each_dic.append(each['name'])
        each_dic.append(each['store_url'])
        each_dic.append(each['comment_degree'])

        for k in each_dic:
            stores_sheet.write(col, row, k)
            row += 1
        col += 1

    goods_sheet.write_merge(0, 0, 0, 2, title)



    base_dir = os.path.dirname(os.path.abspath(__file__))

    filepath = base_dir + '/media/dataexport/' + res_taskid + '.xls'

    if (os.path.exists(filepath)):
        os.remove(filepath)

    wbook.save(filepath)

    return filepath

