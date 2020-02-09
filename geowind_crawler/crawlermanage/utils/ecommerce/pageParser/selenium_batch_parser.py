# -*-coding:utf-8 -*-
from selenium import webdriver
import sys

# from gevent import monkey; monkey.patch_socket()
# import gevent
from time import ctime
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
from crawlermanage.utils.ecommerce.spiderUtils.parser_util import get_soup_by_html_source, get_webdriver
from crawlermanage.utils.ecommerce.spiderUtils.url_utils import url_sifter, get_partial_url
import re
import time
import logging

reload(sys)
sys.setdefaultencoding('utf-8')
"""
1、商品列表页面
"""


# 不需要了，直接replace url中的关键字即可
def get_keyword_methond(url, keyword):
    pass


def get_next_url_by_number123(driver):
    element_1_list = driver.find_elements_by_xpath("//*[text()='1']")
    elsment_2 = ""
    for elem in element_1_list:
        print (elem.tag_name)


def get_next_page_element(driver):
    next_str = u"下一页"
    element = driver.find_element_by_xpath("//*[contains(text(),'%s')]" % next_str)
    element_tag_name = element.tag_name

    if (element_tag_name != "button" and element_tag_name != "a"):
        # 暂时只找一层父节点
        element = element.find_element_by_xpath("..")

    # print element.text
    element.click()
    return driver.current_url

    # return element


# page_url_dic = {}
# [domain.com,domain.cn,domain.net....]
def get_url_domain(url):
    res_url = re.search("\.[0-9a-zA-Z]{2,14}\.(com.cn|com|cn|net|org|wang|cc)", url).group()
    return res_url[1:]


def get_url_by_attrs_dic(driver, attrs_dic):
    find_element_key_list = ['a']
    for key, value in attrs_dic.items():
        if isinstance(value, list):
            continue
        else:
            find_element_key_list.append("[%s='%s']" % (key, value))

    # print "------1------" + ''.join(find_element_key_list)
    elem = driver.find_element_by_css_selector(''.join(find_element_key_list))
    elem.click()
    time.sleep(5)
    return driver.current_url


def get_all_page_number(url):
    print "getallpage_number:" + url
    driver = get_webdriver()

    attemps = 0
    ATTEMPS_TIMES = 3  # 失败尝试3次
    all_page_numer = -1
    while (attemps < ATTEMPS_TIMES and all_page_numer == -1):
        driver.get(url)
        # print driver.page_source
        soup = get_soup_by_html_source(driver.page_source)

        is_find_number = False
        # 当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        element_2_list = soup.find_all("a", text="2")
        for elem in element_2_list:
            find_parent_times = 0
            while (find_parent_times < 4 and is_find_number is False):
                # descendants_list = []
                if (find_parent_times == 0):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.contents
                elif (find_parent_times == 1):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.descendants
                else:
                    elem_ancestor = elem
                    for up_times in range(0, find_parent_times):
                        elem_ancestor = elem_ancestor.parent

                    descendants_list = elem_ancestor.descendants

                for descendant in descendants_list:
                    if (descendant.name != None and descendant.name == 'a'):
                        if descendant.text == '3':
                            is_find_number = True
                        if (is_find_number and descendant.text.isdigit()):
                            # print descendant.text
                            all_page_numer = max(int(descendant.text), all_page_numer)
                    if (is_find_number and descendant.name != None):
                        allpage_text = descendant.parent.parent.parent.text
                        try:
                            tmp_number = int(re.search("\d+", re.search(u"\d+\s*页", allpage_text).group()).group())
                            all_page_numer = max(tmp_number, all_page_numer)
                        except:
                            pass
                            # print tmp_number
                find_parent_times += 1

            if is_find_number and all_page_numer != -1:
                break

        if (is_find_number and all_page_numer != -1):
            break
        else:
            attemps += 1

    driver.close()
    # print (all_page_numer)
    return all_page_numer


"""
通过商品列表的第一个url获取接下来的第二页、第三页
返回值：list[url,urlpage2,urlpag3]
"""
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_next_urlList_by_firstpage_url(url):
    driver = webdriver.PhantomJS()
    # driver = get_webdriver()
    attemps = 0

    ATTEMPS_TIMES = 3  # 失败尝试3次
    FAILUED_STRING = "FAILUED_STRING"
    page_url_list = []
    while (attemps < ATTEMPS_TIMES):
        driver.get(url)
        time.sleep(3)
        print driver.current_url
        # print(driver.page_source)
        soup = get_soup_by_html_source(driver.page_source)
        is_find_page3_url = False
        # 当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        element_2_list = soup.find_all("a", text="2")
        number_to_url_dic = {}
        for elem in element_2_list:
            find_parent_times = 0
            while (find_parent_times < 4 and is_find_page3_url is False):
                # descendants_list = []
                if (find_parent_times == 0):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.contents
                elif (find_parent_times == 1):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.descendants
                else:
                    elem_ancestor = elem
                    for up_times in range(0, find_parent_times):
                        elem_ancestor = elem_ancestor.parent

                    descendants_list = elem_ancestor.descendants

                for descendant in descendants_list:
                    if (descendant.name != None and descendant.name == 'a'):
                        if descendant.text == '3':
                            number_to_url_dic['2'] = elem.get("href")
                            number_to_url_dic['3'] = descendant.get("href")
                            number_to_url_dic['attrs_dic2'] = elem.attrs
                            number_to_url_dic['attrs_dic3'] = descendant.attrs
                            is_find_page3_url = True
                            # print (elem.get("href"))
                            print ("-----------------------------")

                find_parent_times += 1

            if is_find_page3_url:
                break
        next_url_is_fake = False
        # try:
        url_2 = number_to_url_dic['2']
        url_3 = number_to_url_dic['3']
        """
        处理假URL的情况，比如有些URL是#,javascript;这里需要用driver动态跳转，获取current_url
        """
        if (url_2.lower() == url_3.lower()):
            url_2 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic2"])
            url_3 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic3"])

            print "debug:%s" % url_2

            # 出现解析问题，这个url可以跳过
            if (url_2.lower() == url_3.lower()):
                return None

            page_url_list = [url, url_sifter(url, url_2), url_sifter(url, url_3)]
            break
        else:
            page_url_list = [url, url_sifter(url, url_2), url_sifter(url, url_3)]
            break
    driver.close()

    return page_url_list


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pageUrls_and_all_pageNumber(url):
    driver = get_webdriver()
    attemps = 0

    ATTEMPS_TIMES = 3  # 失败尝试3次
    page_url_list = []
    all_page_numer = -1
    while (attemps < ATTEMPS_TIMES):
        driver.get(url)
        time.sleep(3)
        # print(driver.page_source)
        soup = get_soup_by_html_source(driver.page_source)
        is_find_page3_url = False
        # 当前是第一页，寻找分页中的第二页，通过第二页找到第三页的URL
        element_2_list = soup.find_all("a", text="2")
        number_to_url_dic = {}
        for elem in element_2_list:
            find_parent_times = 0
            while (find_parent_times < 4 and is_find_page3_url is False):
                # descendants_list = []
                if (find_parent_times == 0):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.contents
                elif (find_parent_times == 1):
                    elem_parent = elem.parent
                    descendants_list = elem_parent.descendants
                else:
                    elem_ancestor = elem
                    for up_times in range(0, find_parent_times):
                        elem_ancestor = elem_ancestor.parent

                    descendants_list = elem_ancestor.descendants

                for descendant in descendants_list:
                    if (descendant.name != None and descendant.name == 'a'):
                        if descendant.text == '3':
                            number_to_url_dic['2'] = elem.get("href")
                            number_to_url_dic['3'] = descendant.get("href")
                            number_to_url_dic['attrs_dic2'] = elem.attrs
                            number_to_url_dic['attrs_dic3'] = descendant.attrs
                            is_find_page3_url = True
                            # print (elem.get("href"))

                        if (descendant.name != None and descendant.name == 'a'):
                            if descendant.text == '3':
                                is_find_number = True
                            elif (is_find_number and descendant.text.isdigit()):

                                # print descendant.text
                                all_page_numer = max(int(descendant.text), all_page_numer)
                        if (is_find_number and descendant.name != None):
                            allpage_text = descendant.parent.parent.parent.text
                            try:
                                tmp_number = int(re.search("\d+", re.search(u"\d+\s*页", allpage_text).group()).group())
                                all_page_numer = max(tmp_number, all_page_numer)
                            except:
                                pass
                                # print tmp_number

                find_parent_times += 1

            if is_find_page3_url and all_page_numer!=-1:
                break
        # try:
        url_2 = number_to_url_dic['2']
        url_3 = number_to_url_dic['3']
        """
        处理假URL的情况，比如有些URL是#,javascript;这里需要用driver动态跳转，获取current_url
        """
        if (url_2.lower() == url_3.lower()):
            url_2 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic2"])
            url_3 = get_url_by_attrs_dic(driver, number_to_url_dic["attrs_dic3"])

            print "debug:%s" % url_2
            if (url_2.lower() == url_3.lower()):
                return None

            page_url_list = [url, url_sifter(url, url_2), url_sifter(url, url_3)]
            break
        else:
            page_url_list = [url, url_sifter(url, url_2), url_sifter(url, url_3)]
            break

    driver.close()

    return all_page_numer,page_url_list

"""
通过list[url,urlpage2,urlpag3](上一个函数的返回值),获取翻页的信息和关键字信息
返回值：
1、翻页信息,两种情况：
page_name = pagenum (只是一个数字)
page_name = pagemessage (例如0-11-2)
{page_name:[pagenum(第二页的num),dx(差值)]}
{page_name:[pagemessage,{index(第几个数相加（一般是最后一个）):dx}]}


返回值类型：dict

2、查询关键字信息
search_name = keyword
返回值类型:string

例如：
http://search.jumei.com/?filter=0-11-1&search=%E9%9D%A2%E8%86%9C
返回{'filter': ['0-11-2', {2: 1}]},'search'
               value[0]  value[1]
       key          value
"""


# def get_pageKeyDic_and_searchKeywordKey(page_urls,searchKeyword):
def get_pageKeyDic(page_urls):
    url_2 = page_urls[1]
    url_3 = page_urls[2]
    # 获取倒数第二个元素
    url_2_pieces = str(url_2).split("?")[-1].split("&")
    url_3_pieces = str(url_3).split("?")[-1].split("&")
    pieces_2_len = len(url_2_pieces)
    pieces_3_len = len(url_3_pieces)

    """-------------------------返回值-----------------------------"""
    pageKeyDic = {}

    """-----------------------------------------------------------"""

    if pieces_2_len != pieces_3_len:
        raise Exception("解析分页URL碎片时，第二页和第一页URL参数不相等")

    for pieces_index in range(0, pieces_3_len):
        pieces_2_splited = url_2_pieces[pieces_index].split("=")
        pieces_3_splited = url_3_pieces[pieces_index].split("=")

        """
            将page=1这类字符串分割为[page,1],判断第二个值的差，拼接url
            -1是取倒数第一个，当出现只有值不是=分割时，用这种方式比较方便
            存储方式:
            domain.com:{
                            name1:[1(原值，即第二页的值),1(dx,差值)],
                            name2:[0-11-2(原值，即第二页的值),{2:1(dx,差值)}]
                        }

            name2比较特殊，在拥有特殊字符的串中，将0-11-2分割，第2个数字有差值(从0开始)

        """
        if (len(pieces_2_splited) == 2 and pieces_2_splited[-1] != pieces_3_splited[-1]):
            value2 = pieces_2_splited[-1]
            value3 = pieces_3_splited[-1]
            if (value2.isdigit()):
                dx = int(value3) - int(value2)
                pageKeyDic[pieces_2_splited[0]] = [pieces_2_splited[1], dx]


            else:
                value_str_len = min(len(value2), len(value3))
                value2_list = list(value2)
                value3_list = list(value3)
                for ch_index in range(0, value_str_len):
                    if (value2[ch_index].isdigit() is False):
                        value2_list[ch_index] = " "
                    if (value3[ch_index].isdigit() is False):
                        value3_list[ch_index] = " "
                value2 = "".join(value2_list).split(" ")
                value3 = "".join(value3_list).split(" ")

                num_len = len(value2)
                page_index_to_dx = {}
                for num_index in range(0, num_len):
                    if (value2[num_index] != value3[num_index]):
                        page_index_to_dx[num_index] = int(value3[num_index]) - int(value2[num_index])

                pageKeyDic[pieces_2_splited[0]] = [pieces_2_splited[-1], page_index_to_dx]

    # return pageKeyDic,searchKeywordKey
    return pageKeyDic


"""
get_pageKeyList
应对翻页信息重新优化
返回值类型：list

直接替换，例如
http://category.dangdang.com/pg2-cp01.05.12.00.00.00.html
http://category.dangdang.com/pg3-cp01.05.12.00.00.00.html

其中pg3就是翻页信息，我们将原字符串url先用/分割，寻找url2,url3异同的地方



例如：

http://category.dangdang.com/pg2-cp01.05.12.00.00.00.html
http://category.dangdang.com/pg3-cp01.05.12.00.00.00.html
返回[第二个URL的不同处,不同处URL的相同处,第二个URL不同处,不同处的差值]
    [     pg2,          pg,          2        ,   1     ]
"""


def _get_unsame_partstr(list1, list2):
    list_len = len(list1)
    for index in range(list_len):
        if (list1[index] != list2[index]):
            return list1[index], list2[index]

    return None, None


def get_pageKeyList(page_urls):
    url_2 = page_urls[1]
    url_3 = page_urls[2]
    # 获取倒数第二个元素
    url_2_pieces = str(url_2).split("/")
    url_3_pieces = str(url_3).split("/")
    pieces_2_len = len(url_2_pieces)
    pieces_3_len = len(url_3_pieces)

    """-------------------------返回值-----------------------------"""
    pageKeyList = []

    """-----------------------------------------------------------"""

    if pieces_2_len != pieces_3_len:
        raise Exception("解析分页URL碎片时，第二页和第一页URL参数不相等")

    segment_str_2, segment_str_3 = _get_unsame_partstr(url_2_pieces, url_3_pieces)
    segment_str_2_splited = segment_str_2.split('-')
    segment_str_3_splited = segment_str_3.split('-')

    res_unsame_2, res_unsame_3 = _get_unsame_partstr(segment_str_2_splited, segment_str_3_splited)

    page_number_2 = -1
    page_number_3 = -1
    common_previous = ''
    if (res_unsame_2.isdigit()):
        pass
    else:
        index = 0
        res_unsmae_len = len(res_unsame_2)

        while (index < res_unsmae_len):
            if (res_unsame_2[index].isdigit()):
                common_previous = "".join(res_unsame_2[0:index])
                page_number_2 = int("".join(res_unsame_2[index:]))

                page_number_3 = int("".join(res_unsame_3[index:]))
            index += 1

        dx = page_number_3 - page_number_2

        # return pageKeyDic,searchKeywordKey
        pageKeyList = [res_unsame_2, common_previous, page_number_2, dx]
    print
    print pageKeyList
    return pageKeyList


# 必须是第二页之后,返回下一页的url
def get_next_page_by_pageKeyDic_pageUrls_currentPageUrl(pageKeyDic, page_urls, current_page_url):
    # for domain, page_urls in page_url_dic.items():
    url_0 = page_urls[0]
    print (url_0)
    url = page_urls[1]
    url_pageKeyDic = pageKeyDic
    # print url
    previous_attrs_value_dict = {}
    next_url = current_page_url
    for key, value in url_pageKeyDic.items():
        re_str = "%s=(\w-*)+" % key
        page_key_value = re.search(re_str, current_page_url).group()
        if (isinstance(value[1], dict)):
            page_value = page_key_value.split("=")[-1]
            value0_list = list(page_value)
            value0_list_len = len(value0_list)
            ch = " "
            for ch_index in range(0, value0_list_len):
                if (value0_list[ch_index].isdigit() is False):
                    ch = value0_list[ch_index]
                    value0_list[ch_index] = " "

            value0_list_splited = "".join(value0_list).split(" ")
            value0_list_len = len(value0_list_splited)
            for index in range(0, value0_list_len):
                if (value[1].has_key(index)):
                    value0_list_splited[index] = str(int(value0_list_splited[index]) + int(value[1][index]))
            new_page_value = ch.join(value0_list_splited)

        else:
            new_page_value = int(page_key_value.split("=")[-1]) + value[1]

            # print page_key_value, new_page_key_value

        new_page_key_value = "%s=%s" % (page_key_value.split("=")[0], str(new_page_value))
        next_url = next_url.replace(page_key_value, new_page_key_value)

    print ("next = " + next_url)
    return next_url


def get_all_page_urls(pageKeyDic, page_urls, all_page_number):
    url_0 = page_urls[0]
    url = page_urls[1]
    url_pageKeyDic = pageKeyDic
    # print url
    previous_attrs_value_dict = {}
    all_url_list = []
    for i in range(0, all_page_number + 1):
        current_url = url
        for key, value in url_pageKeyDic.items():
            if isinstance(value[1], dict) is True:
                value0_list = list(value[0])
                value0_list_len = len(value0_list)
                ch = " "
                for ch_index in range(0, value0_list_len):
                    if (value0_list[ch_index].isdigit() is False):
                        ch = value0_list[ch_index]
                        value0_list[ch_index] = " "

                value0_list_splited = "".join(value0_list).split(" ")
                value0_list_len = len(value0_list_splited)
                for index in range(0, value0_list_len):
                    if (value[1].has_key(index)):
                        # print "???"
                        if (i == 0):
                            previous_attrs_value_dict[index] = value0_list_splited[index]

                        value0_list_splited[index] = str(int(previous_attrs_value_dict[index]) + int(value[1][index]))

                        previous_attrs_value_dict[index] = value0_list_splited[index]
                        # print previous_attrs_value_dict[index]

                res_value = ch.join(value0_list_splited)
                current_url = current_url.replace(("%s=%s") % (key, value[0]), ("%s=%s") % (key, res_value))


            else:
                if (i == 0):
                    previous_attrs_value_dict[key] = int(value[0])
                current_url = current_url.replace(("%s=%s") % (key, value[0]),
                                                  ("%s=%s") % (key, int(value[1]) + previous_attrs_value_dict[key]))
                previous_attrs_value_dict[key] = int(value[1]) + previous_attrs_value_dict[key]

        if (get_url_domain(url) not in current_url):
            url_sifter(get_partial_url(url_0), current_url)

        all_url_list.append(current_url)
    return all_url_list


"""
例如：

http://category.dangdang.com/pg2-cp01.05.12.00.00.00.html
http://category.dangdang.com/pg3-cp01.05.12.00.00.00.html
返回[第二个URL的不同处,不同处URL的相同处,第二个URL不同处,不同处的差值]
    [     pg2,          pg,          2        ,   1     ]

"""


def get_all_page_urls_by_pageKeyList(pageKeyList, page_urls, all_page_number):
    assert isinstance(pageKeyList, list) and pageKeyList != []

    url_1 = page_urls[0]
    url_2 = page_urls[1]
    pageKeyList = pageKeyList
    # print url
    all_url_list = [url_1, url_2]

    replaced_str = pageKeyList[0]
    common_previous = pageKeyList[1]
    current_key_number = pageKeyList[2]
    dx_number = int(pageKeyList[3])
    for number in range(3, all_page_number):
        current_key_number = int(current_key_number) + dx_number
        next_url = url_2.replace(replaced_str, common_previous + str(current_key_number))
        print next_url

    return all_url_list


def get_nextpage_info(url):
    page_urls = get_next_urlList_by_firstpage_url(url)
    pageKeyDic = get_pageKeyDic(page_urls)
    # print get_next_page_by_pageKeyDic_currentPageUrl_pageKey_and_searchKey(pageKeyDic,page_urls,page_urls[-1])
    get_all_page_urls(pageKeyDic, page_urls, 20)


if __name__ == '__main__':
    print (ctime())


    url = 'http://s.vancl.com/search?k=T%E6%81%A4&orig=3'

    sss = get_next_urlList_by_firstpage_url(url)
    print sss
    # pplist =  get_pageKeyList(sss)
    # get_all_page_urls_by_pageKeyList(pplist,sss,100)
    print (ctime())
