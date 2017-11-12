# -*- encoding: utf-8 -*-
import httplib
import re
import socket
import urllib2

from bs4 import BeautifulSoup
import requests
import sys
from selenium import webdriver
reload(sys)
sys.setdefaultencoding("utf-8")
import time
def get_html(url):
    try:
        obj = requests.get(url)
        statusCod=obj.status_code
        if statusCod == 200:
            code = get_codetype(obj.text)
            if code is not None and code != '':
                obj.encoding = code
            return obj.text
    except socket.timeout, e:
        pass
    except urllib2.URLError,ee:
        pass
    except httplib.BadStatusLine:
        pass

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
    html_str = re.sub('&.{2,5};|&#.{2,5};', '', html_str) #remove special char
    if flag:
        html_str = re.sub('(?is)<.*?>', '', html_str)
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
    title_node = soup.title
    if title_node==None:
        return None
    title = title_node.text
    title = re.sub(r'(-|_)','#', title)
    title = title.split('#')[0]
    if len(title)< 6:
        return None
    return title

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
    time_str = re.search(r'\d{4}(-|\u5E74)(0{0,1}[1-9]|1[0-2])(-|\u6708)(0{0,1}[1-9]|[1-2][0-9]|3[0-1])\u65E5{0,1}', html_str)
    if time_str is not None:
        return time_str.group(0)
    return None

def get_time_by_url(url):
    html = get_html(url)
    time_str = get_time_by_html(html)
    if time_str is None:
        html=get_html_after_selenium(url)
        time_str=get_time_by_html(html)
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
        # print("%s  index结尾"%(href))
        return False
    if len(text.strip()) <= 6:
        # print("%s" %(text))
        # print("%s :标题文本太短"%(href))
        return False
    return True

def is_acricle_page_by_allinfo(html,url,title,time,keywords,content,url_num):
    if title is None:
        # print("标题太短")
        return False
    if url_num > 300:
        # print("%s  url太多"%(url))
        return False
    # if has_special_words(html):
    #     print("%s  有特殊词"%(url))
    #     return False
    if content==None or len(content)<50:
        return False
    return True

def has_special_words(html):
    flag1 = re.findall('<a.*?>.*?阅读.*?</a>', html)
    flag2 = re.findall('<a.*?>.*?查看全文.*?</a>', html)
    # flag3 = re.findall('<a.*?>.*?下一页.*?</a>', html)
    flag3 = re.findall('<iframe.*?>.*?</iframe>', html)
    if len(flag1) > 0:
        # print("阅读")
        return True
    if len(flag2) > 0:
        # print("查看全文")
        return True
    # if len(flag3) > 0:
    #     print("下一页")
    #     return True
    if len(flag3) > 0:
        # print("iframe")
        return True
    return False
    # flag2 = re.search('阅读全文', html)

if __name__ == "__main__":#http://news.sohu.com/s2014/nanshuibeidiao/
    url = "http://tags.blog.sina.com.cn/"
    html = get_html(url)
    print(html)