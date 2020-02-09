from crawlermanage.models import Task, News, Process, Machine, User, Goods, Stores, Blog, TempArticle, Proxy
import logging
from datetime import datetime

import xlwt
def extract():

    res_taskid = '5960a659c5d5860f15e6d470'

    newslist = News.objects.filter(taskid=res_taskid)
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wbook = xlwt.Workbook()
    wsheet = wbook.add_sheet('export data')

    col = 1
    for each in newslist:
        row = 0
        each_dic = dict(each)
        for k in each_dic.keys():
            wsheet.write(col,row,each_dic[k])
            row+=1
        col+=1

    task_message = Task.objects.filter(taskid=res_taskid).get(0)
    title = task_message['taskname']+'('+task_message['starturls'].join(',')+')'


    wbook.save(res_taskid+'.xls')

def get_xls_by_taskid(res_taskid):
    filename = basePath + req.GET['url']

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # response = StreamingHttpResponse(file_iterator(filename))
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response




if __name__ == '__main__':
    extract()