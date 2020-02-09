# -*- encoding: utf-8 -*-
import logging

from crawlermanage.models import Prewebsite
from crawlermanage.utils.message import Message
from crawlermanage.utils.settings_helper import get_attr

logger = logging.getLogger('crawlermanage.views')

def is_open():
    messager = Message(get_attr('LOCAL_HOST'))
    messager.subscribe('crawler')
    msg = 'is_start'
    messager.publish('crawler', msg)
    receive = messager.listen()
    print(receive)
    if receive == 'master:is_start':
        return True
    return False



def import_url(path, type):
    base_dir = get_attr('BASE_DIR')
    absolute_path = base_dir + path

    with open(absolute_path) as f:
        message = f.read()
        logger.info( message)

        f.close()


    for each in  message.split('\n'):
        each_name = each.split(' ')[1]
        each_url = each.split(' ')[0]
        Prewebsite.objects.create(url=each_url, name=each_name, webtype=type)

    logger.info(message)

def import_all():
    import_url(ur"/crawlermanage/static/websitename/blog.txt", ur'blog')
    import_url(ur"/crawlermanage/static/websitename/news.txt", ur'news')
    import_url(ur"/crawlermanage/static/websitename/ecommerce.txt", ur'ecommerce')

if __name__ == '__main__':
    import_all()