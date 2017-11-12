# -*- encoding: utf-8 -*-
import re

'''判断是否为博客或新闻的详情页'''
def is_articel_content_page(url):
    # url_len = len(url)
    if "photo" in url:
        return False


    JUDGE_THRESHOLD = 8
    digit_number = 0
    for ch in url:
        if (str(ch).isdigit()):
            digit_number += 1
    if(digit_number > JUDGE_THRESHOLD):
        return True
    else:return False

def is_articel_content_page_pro(url):
    # url_len = len(url)
    url_splited = url.split("/")
    if len(url_splited) < 4:
        return False

    if "photo" in url:
        return False
    JUDGE_NUMBER_THRESHOLD = 8
    JUDGE_NUMBER_PLUS_CHAR_THRESHOLD  = 12
    digit_number = 0
    up_char_number = 0
    for ch in "".join(url_splited[3:]):
        if (str(ch).isdigit()):
            digit_number += 1
        elif(str(ch).isupper()):
            up_char_number += 1
    if(digit_number > JUDGE_NUMBER_THRESHOLD or (digit_number + up_char_number) > JUDGE_NUMBER_PLUS_CHAR_THRESHOLD):
        return True
    else:
        return False


def is_articel_content_page_blog_and_news(url):
    """
    HTM_NUMBER 以.html或.htm的串:str.html(str.htm) len(str) >HTM_NUMBER
    JUDGE_NUMBER_THRESHOLD 串中数字的个数
    JUDGE_NUMBER_PLUS_CHAR_THRESHOLD 串中数字加大写字符的个数
    """
    HTM_NUMBER = 20
    JUDGE_NUMBER_THRESHOLD = 8
    JUDGE_NUMBER_PLUS_CHAR_THRESHOLD = 12
    # url_len = len(url)
    url_splited = url.split("/")

    # 1
    if len(url_splited) < 4:
        return False

    # 2
    re_str = '\w*\d*.htm'
    re_res = re.search(re_str, url)
    if (re_res != None):
        re_res_len = len(re_res.group())
        if (re_res_len > HTM_NUMBER):
            return True
    # 4
    re_str = '\d{6}'
    re_res = re.search(re_str, '/'.join(url_splited))
    if (re_res != None): return True
    # 5
    if "photo" in url: return False
    if "detail" in url: return True

    digit_number = 0
    up_char_number = 0
    for ch in "".join(url_splited[3:]):
        if (str(ch).isdigit()):
            digit_number += 1
        elif (str(ch).isupper()):
            up_char_number += 1
    if (digit_number > JUDGE_NUMBER_THRESHOLD or (digit_number + up_char_number) > JUDGE_NUMBER_PLUS_CHAR_THRESHOLD):
        return True
    else:
        return False

import random
if __name__ == '__main__':
    # urls_analysis_return_regularly(urls)
    # urls = list(set(urls))
    # for url in urls:
    #     if(is_articel_content_page(url)):
    #         print url
    a = is_articel_content_page_blog_and_news('http://blog.csdn.net/abcjennifer/article/details/42493493')
    print(a)