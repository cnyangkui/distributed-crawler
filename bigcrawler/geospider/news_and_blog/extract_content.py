# -*- encoding: utf-8 -*-
import re
from collections import Counter

from bs4 import BeautifulSoup

from geospider.news_and_blog.article_parser import filter_tags, get_html

authorset = {'责任编辑', '作者'}

'''
    根据文本块密度获取正文
    html_str:网页源代码
    return：正文文本
'''
def extract_content_by_block(html_str):
    html = filter_tags(html_str, True)
    lines = html.split('\n')
    blockwidth = 3
    threshold = 86
    indexDistribution = []

    for i in range(0, len(lines) - blockwidth):
        wordnum = 0
        for j in range(i, i + blockwidth):
            line = re.sub("\\s+", '', lines[j])
            wordnum += len(line)
        indexDistribution.append(wordnum)

    startindex = -1
    endindex = -1
    boolstart = False
    boolend = False
    arcticle_content = []
    for i in range(0, len(indexDistribution) - blockwidth):
        if (indexDistribution[i] > threshold and boolstart is False):
            if indexDistribution[i + 1] != 0 or indexDistribution[i + 2] != 0 or indexDistribution[i + 3] != 0:
                boolstart = True
                startindex = i
                # print 'startindex=%d' %startindex
                continue
        if boolstart is True:
            if indexDistribution[i] == 0 or indexDistribution[i + 1] == 0:
                endindex = i
                # print 'endindex=%d' % endindex
                boolend = True
        tmp = []
        # print("%d %d"%(startindex,endindex))
        if boolend is True:
            for index in range(startindex, endindex + 1):
                line = lines[index]
                if len(line.strip()) < 5:
                    continue
                tmp.append(line.strip() + '\n')
            tmp_str = ''.join(tmp)
            if u"Copyright" in tmp_str or u"版权所有" in tmp_str:
                continue
            arcticle_content.append(tmp_str)
            boolstart = False
            boolend = False
    return ''.join(arcticle_content)

'''
    全网页查找根据文本块密度获取的正文，获取文本父级标签获取正文
    html:网页html
    article:根据文本块密度获取的正文
    return:正文文本
'''
def extract_content_by_tag(html_str, article):
    lines = filter_tags(html_str, False)
    soup = BeautifulSoup(lines, 'lxml')
    p_list = soup.find_all('p')
    p_in_article = []
    for p in p_list:
        if p.text.strip() in article:
            p_in_article.append(p.parent)
    tuple = Counter(p_in_article).most_common(1)[0]
    article_soup = BeautifulSoup(str(tuple[0]), 'xml')
    return remove_space(article_soup.text)
    # print(tuple[0])
    # return remove_space_from_text(article_soup.text)

def remove_space(text):
    text = re.sub("[\t\r\n\f]", '', text)
    # text=text.replace('　','')
    return text

'''
    抽取正文
    html_str:网页源代码
    return：正文文本
'''
def extract_content(html_str):
    article_temp = extract_content_by_block(html_str)
    try:
        article = extract_content_by_tag(html_str, article_temp)
    except:
        article = article_temp
    return article

if __name__ == '__main__':
    url = 'http://news_and_blog.qq.com/a/20170126/018592.htm'
    html = get_html(url)
    a  = extract_content(html)
    print(a)