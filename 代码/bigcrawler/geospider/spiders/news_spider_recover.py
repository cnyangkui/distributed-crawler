# -*- encoding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request

from geospider.news_and_blog.article_parser import *
from geospider.items import News
import sys

from geospider.utils.mongodb_helper import connect_mongodb, NewsDao

reload(sys)
sys.setdefaultencoding("utf-8")
from geospider.news_and_blog.extract_content import extract_content
from geospider.utils.url_util import is_articel_content_page_blog_and_news


class NewsSpiderRecover(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'news_recover'
    redis_key = 'news_recover:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        print("***********************************************************8")
        #self.allowed_domains = filter(None, domain.split(','))
        db = connect_mongodb()
        newsdao = NewsDao(db)
        taskid = self.redis_key.split(':')[0]
        self.url_list_download = newsdao.find_urls_by_taksid(taskid)
        super(NewsSpiderRecover, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield Request(url=response.url, callback=self.parse_page)

    def parse_page(self, response):
        a_list = response.xpath(
            "//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        for a in a_list:
            item_href = ''.join(a.xpath("./@href").extract()).strip()
            item_text = ''.join(a.xpath("./text()").extract()).strip()
            flag = is_articel_content_page_blog_and_news(item_href)
            if flag:
                yield Request(url=item_href, callback=self.parse_acticle)
            else:
                yield Request(url=item_href, callback=self.parse_page)


    def parse_acticle(self, response):
        html = get_html(response.url)
        article = extract_content(html)
        title = get_title(html)
        time = get_time_by_html(html)
        keywords = get_keywords(html)
        url_num = len(get_all_url(html))

        flag = is_acricle_page_by_allinfo(html,title,keywords,article,url_num)

        if flag:
            item = News()
            item['url'] = str(response.url)
            item['title'] = str(title)
            item['time'] = str(time)
            item['keywords'] = str(keywords)
            item['article'] = str(article)
            item['taskid'] = str(self.name)
            if response.url not in self.url_list_download:
                yield item

