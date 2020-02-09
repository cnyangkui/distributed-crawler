# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from crawlermanage.utils.ecommerce.spiderUtils.parser_util import get_soup_by_html_source,\
    get_soup_by_selenium_without_script,get_soup_by_request_without_script


from crawlermanage.utils.ecommerce.spiderUtils.url_utils import url_sifter
from crawlermanage.utils.ecommerce.pageParser.category_page_parser import category_page_parser


from urllib2 import quote,unquote
import os
#计算得分
"""
给出一定的关键词，计算某个组建的关键词得分，得分高的作为navbar，存在一定失败率
"""
def get_nav_by_keyword_scoring(container,indexURL):
    # featureDict = load_keyword_file('e-commerce.txt')
    FILEPATH = project_dir = os.path.dirname(os.path.abspath(__file__))
    featureDict = load_keyword_file('%s/e-commerce.txt'%FILEPATH)
    scoreList = []
    javascript_num_list =[]
    index = 0
    fitting_index = 0
    fitting_score = -1

    # 避免url不完整的情况 step1
    # 这里还有问题，比如http://club.yhd.com/这恶果网站，以club开头
    url_domain = ''
    if 'https://www.' in indexURL:
        url_domain = indexURL.replace('https://www.','')
    elif "http://www." in indexURL:
        url_domain = indexURL.replace('http://www.', '')
    for ul in container:
        # print "---" + str(ul)
        score = 0
        url_with_javascript_number = 0
        soup2 = BeautifulSoup(str(ul), 'lxml')
        # find out all <a> tag of one <ul>
        alist = soup2.find_all('a')
        # if len(alist) != 0:
        for a in alist:
            if(a.name is None) :continue

            # soup3 = BeautifulSoup(str(a).strip(), 'lxml')
            # print ("soup =  "+ str(soup3))
            content = a.text.encode('utf8')

            try:
                if( "javascript" in a['href']):
                    # print soup3.a.get("href")
                    url_with_javascript_number +=1
            except:
                pass

            # print href_list
            # if content != '' and content is not None and href !='' and href is not None:
            if content != '' and content is not None :
                # and len(href_list) != 0 and str(href_list[0]) != ''
                for key in featureDict.keys():
                    # print(str(key))
                    if str(content) in str(key) or str(key) in str(content):
                        score += int(featureDict.get(key))
                        # print  content
                        break

        # print "score=%d,fitting_score=%d" %(score,fitting_score)
        scoreList.append(score)
        javascript_num_list.append(url_with_javascript_number)
        if fitting_score < score:

            fitting_index = index
            fitting_score = score

        index += 1

    # 符合
    # log_util.info( "final fitting_score=%d"%fitting_score)
    # log_util.info( "len(scoreList) = %d" % len(scoreList))
    # log_util.info( "url_with_javascript_number = %d"% (javascript_num_list[fitting_index]))
    """
    socreList 保证当前遍历列表不为空
    fitting_socre 匹配关键字数目 不小与 4
    url_with_javascript_number 在url中的javascript字符串数目 应该小于 5
    
    """

    if(len(scoreList)>0 and fitting_score >= 4 and(javascript_num_list[fitting_index]) < 5):
        return container[fitting_index]
    else:return None


#加载特征数据
def load_keyword_file(fileName):
    fr = open(fileName, 'r')
    arrayLines = fr.readlines()
    featureDict = {}
    for line in arrayLines:
        line = line.strip()
        line = line.split(' ')
        featureDict[line[0]] = line[1]
        #print line[0]+" "+line[1]
    return featureDict


# strategy1 寻找所有分类（大分类页）
# strategy e-commerce get link from the keyword = "分类" or "商品分类"
# 返回一个url或空值，空即是没找到，执行下一步
def get_allCategory_from_Key(soup):
    keyword = [u"全部商品分类",u"商品分类",u"全部分类",u"分类",]
    for label_i in range(0, 4):
        a_key = soup.find_all(True, text=re.compile(keyword[label_i]))
        # print a_key
        # print soup.prettify()
        # print a_key
        for a in a_key:
            # print  a
            if "</script>" in str(a):
                # print re.findall("{.+?}",str(a))
                for tmp in re.findall("{.+?}",str(a)):
                    if(keyword[label_i] in str(tmp)):
                        key_value = tmp.split(",")
                        for kv in key_value:
                            tmp_kv = kv.split(":")
                            key = tmp_kv[0]
                            value = tmp_kv[1]
                            #能否判断value是url,不能就用以下方法
                            if key =='"url"' :
                                return value
            else:
                deep = 1
                a_copy = a
                while(deep < 5):
                    soup_tmp = BeautifulSoup(str(a_copy), "lxml")
                    res_a= soup_tmp.find_all("a")
                    if len(res_a)!=0:
                        for a_list in res_a :
                            return a_list.get("href")
                        break

                    a_copy = a_copy.parent
                    # print  a_copy
                    deep += 1

    for label_i in range(0, 4):
        for sin_a in soup.find_all("a"):
             if keyword[label_i] in str(sin_a):
                  return sin_a.get("href")

    return None


# strategy2 class = nav
def get_nav_by_class_nav(soup,url):
    all_element = soup.find_all("ul",class_= re.compile("nav"))
    navUl = get_nav_by_keyword_scoring(all_element, url)
    if navUl is None:
        all_element = soup.find_all("div",class_= re.compile("nav"))
        navUl = get_nav_by_keyword_scoring(all_element, url)

    return navUl

# strategy3 all by select ul
def get_nav_by_tag_ul(soup,url):
    all_ul = soup.find_all('ul')
    return get_nav_by_keyword_scoring(all_ul, url)

# strategy4 还未完成，需要找子节点
def get_nav_by_tag_div(soup,url):
    all_div = soup.find_all('div')
    get_nav_by_keyword_scoring(all_div, url)

def debug(debug_info):
    print ("debug:%s"%debug_info)


def get_categoryList_method_in_index_url(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    allCategory_page_url = get_allCategory_from_Key(soup=soup)
    # method = 1
    if (allCategory_page_url != None):
        """
        这里实际上是进入下一页页面，一般写callback
        """
        allCategory_page_url = url_sifter(url, allCategory_page_url)
        # print (allCategory_page_url)
        url_list = category_page_parser(allCategory_page_url)
        # print (len(url_list))

    else:
        pass

# 将 [[a1,url1],[a2,url3]....]的形式保存下来
def get_aTag_url_integration(original_data,domain):
    tmp_soup = get_soup_by_html_source(str(original_data))
    a_list = tmp_soup.find_all("a")
    # print (a_list)
    a_url_res = []
    for tag in a_list:
        a_url_res.append([tag.text,url_sifter(domain,tag.get("href"))])

    # print (a_url_res)
    return a_url_res

"""
method 用以鉴别当前方法使用一般的request还是selenium方法解析html
selenium解析相对较慢，所以一般用request解析
request method == 1
selenium method == 2

soup  当前页的解析
url   主页url
methon
"""
def get_nav_in_url(soup, url,parser_method):
    allCategory_page_url = get_allCategory_from_Key(soup=soup)

    # 方法一：获取大分类页面
    if (allCategory_page_url != None and "javascript" not in allCategory_page_url):
        # log_util.error("大分类页面：" + allCategory_page_url)

        allCategory_page_url = url_sifter(url, allCategory_page_url)
        # print ("大分类页面：" + allCategory_page_url)
        # print ("解析方法：%d,%d" % (parser_method, 1))
        # if(methon == 2):
        #     next_soup = get_soup_by_selenium_with_sleep(allCategory_page_url)
        # else:next_soup = get_soup_by_request(url)

        a_url_list = category_page_parser(allCategory_page_url, url,parser_method)
        return 1, a_url_list
    else:
        nav = get_nav_by_class_nav(soup,url)
        if nav == None:
            nav = get_nav_by_tag_ul(soup,url)
            # print nav
            way_number = 3
        else:
            way_number = 2

        if nav == None:
            return -1, None
        else:
            # print ("解析方法：%d,%d"%(parser_method,way_number))
            return way_number, get_aTag_url_integration(nav, url)

"""
request method == 1
selenium method == 2
"""
def get_aTag_nav_by_request(url):
    soup = get_soup_by_request_without_script(url)
    # print soup.prettify()
    return get_nav_in_url(soup,url,1)

def get_aTag_nav_by_selenium(url):
    soup = get_soup_by_selenium_without_script(url)
    return get_nav_in_url(soup,url,2)


"""
get_deep 表示当前对某个网页进行了几次获取nav了，即获取nav的深度。
默认：一般以非大页面类获取的nav都有子目录，所有以进行一次获取nav

"""

def mylist_set(_list):

    url_set = set()
    res_list = []
    for each in _list:
        url = each[1]
        if(url != None and url!= '' and url not in url_set):
            url_set.add(url)
            res_list.append(each)
        # else:
        #     print 'common'

    return res_list

def get_nav(url,get_deep):
    method,nav = get_aTag_nav_by_request(url)
    if(method==-1):
        # return get_aTag_nav_by_selenium(url)
        method, nav = get_aTag_nav_by_selenium(url)
    # else:
    #     return method,nav
    len_of_nav = len(nav)
    if method!= 1 and get_deep==0:
        # if(get_deep==0):
        nav_list = []
        for ttpp in nav:
            next_url = ttpp[1]
            method_2,nav_2 = get_nav(next_url,1)
            # print nav_2
            if(method_2 == 1 and len(nav_2) > len_of_nav):
                nav_list = nav_2
                break
            elif(method_2!=-1):
                nav_list.extend(nav_2)

        # return 1,list(set(nav_list))
        return 1,mylist_set(nav_list)
    else:
        return method,mylist_set(nav)


def deep_search_get_searchUrl_and_keyword_in_soup(soup,url):
    res_url = None
    res_key = None
    res_method = ""
    for a in soup.find_all('a'):
        try:
            next_url = a.get('href')
            # and quote(a.text) in next_url
            http_code_key = quote(a.text.encode('utf-8'))
            origianl_key = a.text
            if (next_url != None and 'javascript' not in next_url and http_code_key != None
                and http_code_key != '' and origianl_key != None and origianl_key != ''):
                # and http_code_key != None
                # and http_code_key != '' and origianl_key != None
                if ('search' in next_url):

                    if (origianl_key in next_url ):
                        res_url = next_url
                        res_key = origianl_key
                        res_method = "ORIGINALKEY"
                        break
                    if(http_code_key in next_url):
                        res_url = next_url
                        res_key = http_code_key
                        res_method = "HTTPENCODEKEY"
                        break

                    re_str = '(%[\w\d]{2,4}\d*)+'
                    # print next_url
                    if (re.search(re_str, next_url)):
                        res_key =  re.search(re_str, next_url).group()
                        res_url =  next_url
                        res_method = "REGULARHTTP"

                        break
        except:
            pass

    # print res_url
    return [url_sifter(parent_url=url,url=res_url),res_key,res_method]

def get_searchUrl_and_keyword(p_soup,url):
    # soup = get_soup_by_request_without_script(url)
    res_list = deep_search_get_searchUrl_and_keyword_in_soup(p_soup,url)
    if(res_list[0] == None):
        soup = get_soup_by_selenium_without_script(url)
        res_list = deep_search_get_searchUrl_and_keyword_in_soup(soup,url)

    return res_list

"""

1、原串中本来就含有key

2、正则http编码的字符串

"""

if __name__ == '__main__':

    url = 'https://www.taobao.com/'
    # 当当
    # url = "http://www.dangdang.com/"
    # 唯品会
    # url = "http://www.vip.com/"
    # 凡客诚品
    # url = "http://www.vancl.com/"
    # 一号店
    # url = "http://www.yhd.com/"
    # 亚马逊
    # url = "https://www.amazon.cn/"
    # 美丽说
    # url = "http://www.meilishuo.com/"
    #
    # url = "https://www.jd.com/"
    # url = 'http://www.mogujie.com'

    # url ='https://www.tmall.com/'


    # print get_searchUrl_and_keyword(get_soup_by_request_without_script(url),url)
    print get_nav(url,0)

    pass