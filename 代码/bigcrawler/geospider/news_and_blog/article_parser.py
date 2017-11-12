# -*- encoding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import sys
from selenium import webdriver
# reload(sys)
# sys.setdefaultencoding("utf-8")
authorset = {'责任编辑', '作者'}

def get_html(url):
    # driver = webdriver.PhantomJS()
    # driver.get(url)
    obj = requests.get(url)
    code = get_codetype(obj.text)
    if code is not None and code != '':
        obj.encoding = code
    return obj.text

def get_html_after_selenium(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    html_source = browser.page_source
    browser.close()
    return html_source

def filter_tags(html_str, flag):
    html_str = re.sub('(?is)<!DOCTYPE.*?>', '', html_str)
    html_str = re.sub('(?is)<!--.*?-->', '', html_str) #remove html comment
    html_str = re.sub('(?is)<script.*?>.*?</script>', '', html_str) #remove javascript
    html_str = re.sub('(?is)<style.*?>.*?</style>', '', html_str) #remove css
    html_str = re.sub('(?is)<a[\t|\n|\r|\f].*?>.*?</a>', '', html_str)  # remove a
    html_str = re.sub('(?is)<li[^nk].*?>.*?</li>', '', html_str)  # remove li
    #html_str = re.sub('&.{2,5};|&#.{2,5};', '', html_str) #remove special char
    if flag:
        html_str = re.sub('(?is)<.*?>', '', html_str) #remove tag
    return html_str

#获取编码类型
def get_codetype(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    meta = soup.find_all('meta')
    codetype = ''
    for m in meta:
        name = m.get('http-equiv')
        if name is not None:
            if str(name).lower() == 'content-type':
                charset = str(m.get('content')).lower()
                if 'charset=gb2312' in charset:
                    codetype = 'gb2312'
                    break
                elif 'charset=utf-8' in charset:
                    codetype = 'utf-8'
                    break
                elif 'charset=gbk' in charset:
                    codetype = 'gbk'
                    break
    if codetype == '':
        for m in meta:
            charset = m.get('charset')
            if charset is not None:
                if 'gb2312'==charset:
                    codetype = 'gb2312'
                    break
                elif 'utf-8'==charset:
                    codetype = 'utf-8'
                    break
                elif 'gbk'==charset:
                    codetype = 'gbk'
                    break
    return codetype

#获取标题
def get_title(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    title = soup.title.text
    title = re.sub(r'(-|_)','#', title)
    title = title.split('#')[0]
    # print(title)
    if(len(title.strip())>=8):
        return title
    return None

#获取关键词
def get_keywords(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    keywords = None
    meta = soup.find_all('meta')
    for m in meta:
        name = str(m.get('name')).lower()
        if name=='keywords':
            keywords = m.get('content')
            break
    return keywords


def get_img(html_str):
    pass

#获取时间
def get_time_by_html(html_str):
    time_str = re.search(ur'\d{4}(-|\u5E74)\d{1,2}(-|\u6708)\d{1,2}\u65E5{0,1}', html_str)
    if time_str is not None:
        return time_str.group(0)
    return None

def get_time_by_url(url):
    html = get_html(url)
    time_str = get_time_by_html(html)
    # if time_str is None:
    #     html=get_html_after_selenium(url)
    #     time_str=get_time_by_html(html)
    return time_str

def get_all_url(html_str):
    soup = BeautifulSoup(html_str, 'lxml')
    alist = soup.find_all('a')
    href_list = []
    for a in alist:
        href = a.get('href')
        # print (a.text+" "+href)
        if href is not None and href !='':
            if href.startswith('javascript') or href.endswith('.jpg') or href.endswith('.png') or href.endswith('.jpeg') \
                    or href.endswith('gif') or href.endswith('.pdf'):
                continue
            else:
                href_list.append(href)

    return href_list

def is_acricle_page_by_url_and_text(href, text):
    # print("%s %s"%(href, text))
    if href.endswith("index.html") or href.endswith("index.shtml") or href.endswith("index.htm"):
        # print("index结尾")
        return False
    if len(text.strip()) < 6:
        # print("%s" %(text))
        # print("标题文本太短")
        return False
    return True

def is_acricle_page_by_allinfo(html,title,keywords,content,url_num):
    if title is None:
        # print("标题太短")
        return False
    if content is None or len(content.strip())<20:
        # print("正文太短")
        return False
    if url_num > 300:
        # print("url太多")
        return False
    if has_special_words(html):
        # print("有特殊词")
        return False
    return True

def has_special_words(html):
    flag1 = re.findall('<a.*?>.*?下一页.*?</a>', html)
    flag2 = re.findall('<a.*?>.*?阅读全文.*?</a>', html)
    if len(flag1) > 0:
        return True
    if len(flag2) > 0:
        return True
    return False
    # flag2 = re.search('阅读全文', html)
from urllib2 import quote
if __name__ == "__main__":#http://news.sohu.com/s2014/nanshuibeidiao/
    # url = quote("http://tags.blog.sina.com.cn/花千骨")
    # url = url.replace('%3A',':')
    # print url
    # html = get_html(url)
    url = 'http://news_and_blog.qq.com/a/20170624/015461.htm'
    html = get_html(url)
    time = get_time_by_html(html)
    print(time)
