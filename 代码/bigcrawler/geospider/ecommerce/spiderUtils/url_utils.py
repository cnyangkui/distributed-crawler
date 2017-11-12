#coding:utf-8

import re
import pprint
from difflib import SequenceMatcher
from cluster import HierarchicalClustering


# class URLUtils:
    # def __init__(self):
    #     pass
"""
原始的url_sifter，做备份
"""
# def url_sifter(parent_url, url):
#     # print parent_url
#     # print url
#     if url is None or len(url) == 0:
#         return None
#
#     cu_url = str(url)
#     cuURL_len = len(cu_url)
#     pa_url = str(parent_url)
#     paURL_len = len(pa_url)
#     #  去除双引号
#     cu_url   = cu_url.replace('"',"")
#     #  去掉开头的／或//
#     if (cu_url.startswith("/")):
#         if (cu_url.startswith("//")):
#             index = 2
#             for ind in range(2, cuURL_len):
#                 if (cu_url[ind] is not '/'):
#                     index = ind
#                     break
#
#             cu_url = cu_url[index:cuURL_len]
#         else:
#             cu_url = cu_url[1:cuURL_len]
#
#     pa_part = pa_url.split('.')
#     part_len = len(pa_part)
#     domain = ""
#     if part_len == 2:
#         domain = pa_part[0]
#     elif part_len == 3:
#         domain = pa_part[1]
#     # domain = get_url_domain(pa_url)
#     # print domain
#     if domain not in cu_url:
#         print '6666'
#         cu_url = pa_url + ('' if pa_url[paURL_len - 1] == '/' else '/') + cu_url
#
#     if "https://" not in cu_url and "http://" not in cu_url:
#         http_str_header = pa_url.split("//")
#         cu_url = http_str_header[0] + "//" + cu_url
#
#     return cu_url




#通过上下文信息，拼接一些非法的url,例如//xxx.com等等
# "xxxx"
def url_sifter(parent_url, url):
    # print parent_url
    # print url
    if url is None or len(url) == 0:
        return None

    cu_url = str(url)
    cuURL_len = len(cu_url)
    pa_url = str(parent_url)
    paURL_len = len(pa_url)
    #  去除双引号
    cu_url   = cu_url.replace('"',"")
    #  去掉开头的／或//
    if (cu_url.startswith("/")):
        if (cu_url.startswith("//")):
            index = 2
            for ind in range(2, cuURL_len):
                if (cu_url[ind] is not '/'):
                    index = ind
                    break

            cu_url = cu_url[index:cuURL_len]
        else:
            cu_url = cu_url[1:cuURL_len]


    domain = get_url_domain(pa_url)
    # print domain
    if domain not in cu_url:
        pre_url  =  get_partial_url(pa_url)
        cu_url = pre_url + ('' if pa_url[paURL_len - 1] == '/' else '/') + cu_url

    if "https://" not in cu_url and "http://" not in cu_url:
        http_str_header = pa_url.split("//")
        cu_url = http_str_header[0] + "//" + cu_url

    return cu_url


def pic_url_sifter(parent_url,pic_url):

    if pic_url is None or len(pic_url) == 0:
        return None

    cu_url = str(pic_url)
    cuURL_len = len(cu_url)
    pa_url = str(parent_url)
    cu_url   = cu_url.replace('"',"")
    #  去掉开头的／或//
    if (cu_url.startswith("/")):
        if (cu_url.startswith("//")):
            index = 2
            for ind in range(2, cuURL_len):
                if (cu_url[ind] is not '/'):
                    index = ind
                    break

            cu_url = cu_url[index:cuURL_len]
        else:
            cu_url = cu_url[1:cuURL_len]

    if "https://" not in cu_url and "http://" not in cu_url:
        http_str_header = pa_url.split("//")
        cu_url = http_str_header[0] + "//" + cu_url

    return cu_url



def get_url_domain(url):
    res_url = re.search("\.[0-9a-zA-Z]{2,14}\.(com.cn|com|cn|net|org|wang|cc)",url).group()
    return res_url[1:]
# 截取前一段url
def get_partial_url(url):
    res_url = re.search(".+\.(com.cn|com|cn|net|org|wang|cc)", url).group()
    return res_url

def urls_clustering(urls):
    # 输入 urls
    # 计算url之间的距离
    # 使用difflib中的SequenceMatcher计算
    def distance(url1, url2):
        ratio = SequenceMatcher(None, url1, url2).ratio()
        return 1.0 - ratio

    # 执行层次聚类
    hc = HierarchicalClustering(urls, distance)
    clusters = hc.getlevel(0.2)
    # pprint.pprint(clusters)

    return clusters

def get_domain(url):
    domain = url.split('/')[2]
    if domain.startswith('www'):
        return get_url_domain(url)
    return domain

if __name__ == '__main__':
    print(get_partial_url('http://news.qq.com/gsdfgsd/fdsf/sdfsd/sdf'))
    print(get_url_domain('http://www.people.com.cn/'))
    print(get_domain('http://www.xinhuanet.com/'))
    print(get_domain('http://news.qq.com/gsdfgsd/fdsf/sdfsd/sdf'))
    # print x.bit_length()