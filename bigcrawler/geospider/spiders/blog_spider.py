# -*- encoding: utf-8 -*-
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider

from geospider.news_and_blog.article_parser import *
from geospider.items import Blog
from geospider.news_and_blog.extract_content import extract_content
from geospider.utils.url_util import is_articel_content_page_blog_and_news
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class BlogSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'blog'
    redis_key = 'blog:start_urls'

    # rules = (
    #     # follow all links
    #     Rule(domain_rule, callback='parse_page', follow=True),
    # )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        print("***********************************************************")
        #print(domain)
        #self.allowed_domains = filter(None, domain.split(','))
        # self.allowed_domains=['blog.sina.com.cn']
        super(BlogSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        yield Request(url=response.url, callback=self.parse_page)

    def parse_page(self, response):
        # print("ccccc:" + response.url)
        a_list = response.xpath(
            "//a[(starts-with(@href,'http') or starts-with(@href, 'https')) and string-length(text())>0]")
        #print("href:%s num:%d" % (response.url, len(a_list)))
        for a in a_list:
            item_href = ''.join(a.xpath("./@href").extract()).strip()
            item_text = ''.join(a.xpath("./text()").extract()).strip()
            flag = is_articel_content_page_blog_and_news(item_href)
            if flag:
                # print('a'+item_text)
                yield Request(url=item_href, callback=self.parse_acticle)
            else:
                # print("b:"+item_text)
                yield Request(url=item_href, callback=self.parse_page)


    def parse_acticle(self, response):
        # print("parse_acticle:"+response.url)
        html = get_html(response.url)
        article = extract_content(html)
        title = get_title(html)
        time = get_time_by_html(html)
        keywords = get_keywords(html)
        url_num = len(get_all_url(html))

        flag = is_acricle_page_by_allinfo(html,title,keywords,article,url_num)

        if flag:
            # print("parse successful......%s"%(response.url))
            item = Blog()
            item['url'] = str(response.url)
            item['title'] = str(title)
            item['time'] = str(time)
            item['keywords'] = str(keywords)
            item['article'] = str(article)
            item['taskid'] = str(self.name)
            yield item