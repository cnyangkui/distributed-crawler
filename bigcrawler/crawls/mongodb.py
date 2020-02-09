import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
if __name__ == '__main__':
    url = 'http://news.hao123.com/wangzhi'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'lxml')
    # print soup.prettify()

    print len(soup.find_all('ul',class_='content-link'))
    cnt = 0
    for each_ul in soup.find_all('ul',class_='content-link'):
        if(cnt >= 2): break
        cnt += 1
        for each_tag in each_ul:
            a_tag =  each_tag.find('a')
            print a_tag['href'],a_tag.text

    # for each_tag in soup.find('ul',class_='content-link'):
    #     # print each_tag
    #     # for index in range(0,2):
    #     # print each_tag
    #     a_tag =  each_tag.find('a')
    #     print a_tag['href'],a_tag.text