#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup,Comment
import requests
from geospider.ecommerce.spiderUtils.url_utils import url_sifter
from geospider.ecommerce.spiderEntiy.category_item import category_item
from geospider.ecommerce.spiderUtils.parser_util import get_soup_by_selenium_with_sleep,get_soup_by_request
# url = "https://www.taobao.com/tbhome/page/market-list"
import time

def get_tag_path(tag):
    parent_tag = tag.parent
    tag_path_stack = []
    tag_path_stack.append("/%s" % tag.name)
    while parent_tag != None and parent_tag.name != None:
        if (parent_tag.name == "html"):
            tag_path_stack.append("%s" % parent_tag.name)
            break

        tag_path_stack.append("/%s" % parent_tag.name)
        parent_tag = parent_tag.parent

    tag_path_stack.reverse()
    tag_path = "".join(tag_path_stack)

    return tag_path

# domain 是首页
def category_page_parser(url,domain,parser_method):
    if parser_method == 1:
        soup = get_soup_by_request(url)
        # soup = BeautifulSoup(resq.text,"lxml")
    else:
        soup = get_soup_by_selenium_with_sleep(url)

    # print soup.prettify()

    tagPath_to_appearCount = {}
    tagPath_to_allTagInPath = {}

    max_appear_tag_path = ""
    max_appear_tag_number = 0

    for current_tag in soup.find_all("a"):

        # get 'tag-path' such as html/body/div/div/ul/li/a
        tag_path = get_tag_path(current_tag)

        # Has 'tag-path' been appeared
        if(tag_path in tagPath_to_appearCount):
            tagPath_to_appearCount[tag_path] +=1
            tagPath_to_allTagInPath[tag_path].append(current_tag)
        else:
            tagPath_to_appearCount[tag_path] = 1
            tagPath_to_allTagInPath[tag_path] = []
            tagPath_to_allTagInPath[tag_path].append(current_tag)

    sorted_tag_path_list = sorted(tagPath_to_appearCount.items(), key=lambda d: d[1], reverse=True)
    # for item in sort:
    #     print  "%s %s" % (sorted_tag_path_list[0], sorted_tag_path_list[1])

    # all_category = tagPath_to_allTagInPath[sorted_tag_path_list[0][0]]
    # category_res_list = []
    # category_name_set = set()

    # for tag in all_category:
    #     # if(category_name_set)
    #     # parent_deep =  1
    #     #
    #     # while(parent_deep <=3 and tag.text != None and len(tag.text)!=0):
    #     #
    #     #
    #     #
    #     #     parent_deep+=1
    #
    #
    #     print "-----------one menu----------------"
    #
    #     parent_tag = tag.parent
    #     # print parent_tag.text
    #
    #
    #
    #     parent_tag = parent_tag.parent
    #     # print parent_tag.text
    #     #
    #     parent_tag = parent_tag.parent
    #     print parent_tag.text
    #     print "-----------one menu----------------"
    #     # while parent_tag != None and parent_tag.name != None:
    #

    # parent_threshold_num = sorted_tag_path_list[int(len(sorted_tag_path_list)/3)][1]
    # category_menu_1_list = []
    #
    # print parent_threshold_num
    sorted(tagPath_to_appearCount.items(), key=lambda d: d[1])
    for key, value in tagPath_to_appearCount.items():
        # print key, ':', value
        if(max_appear_tag_number < value):
            max_appear_tag_number = value
            max_appear_tag_path = key

    all_category_tag_list = tagPath_to_allTagInPath[max_appear_tag_path]
    print (len(all_category_tag_list))


    a_url_list = []
    for tag in all_category_tag_list:
        # print tag.text
        a_url_list.append([tag.text,url_sifter(domain,tag.get("href"))])

    return a_url_list


    # all_category_url_list = []
    # for tag in all_category_tag_list:
    #     all_category_url_list.append(tag.get("href"))
    # return all_category_url_list