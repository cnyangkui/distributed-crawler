# -*- encoding: utf-8 -*-
import re
from bs4 import BeautifulSoup, Comment
import requests
authorset = {'责任编辑', '作者'}

nodes = []
msg_len = []

def getcontentfromweb(url):
    obj = requests.get(url)
    #code = requests.head(url).encoding
    code = getcodetype(obj.text)
    if code is not None and code != '':
        obj.encoding = code
    return obj.text


def traversal_brother(obj):

    reg1 = re.compile("<[^>]*>")

    next_soup = BeautifulSoup(str(obj), 'lxml')
    res = reg1.sub('', next_soup.prettify()).split('\n')
    content = ''.join(res)
    print(str(len(content))+" "+content)
    nodes.append(obj)
    msg_len.append(len(content))

    next = obj.next_sibling
    while next != None:
        next_soup = BeautifulSoup(str(next), 'lxml')
        res = reg1.sub('', next_soup.prettify()).split('\n')
        content = ''.join(res)
        print(str(len(content)) + " " + content)
        nodes.append(next)
        msg_len.append(len(content))
        next = next.next_sibling




def parser(obj):
    soup = BeautifulSoup(obj, 'lxml')
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]

    reg1 = re.compile("<[^>]*>")

    title = soup.h1
    content = reg1.sub('', title.prettify()).split('\n')
    print (''.join(content).strip())
    print("*******************************8")

    traversal_brother(title)
    parent = title.parent
    traversal_brother(parent)

    max_index = msg_len.index(max(msg_len))
    max_node = nodes[max_index]

    first_child = max_node.contents[0]
    while first_child.name != 'p':
        del nodes[:]
        del msg_len[:]
        traversal_brother(first_child)
        max_index = msg_len.index(max(msg_len))
        max_node = nodes[max_index]
        first_child = max_node.contents[0]


    for n in nodes:
        print(n)
        print("======================")

    # next = title.next_sibling
    # next_soup = BeautifulSoup(str(next), 'lxml')
    # content = reg1.sub('', next_soup.prettify()).split('\n')
    # if len(content) > 30:
    #     msg.append(''.join(content))
    #     msg_len.append(len(msg))
    # while next != None:
    #     next = next.next_sibling
    #     next_soup = BeautifulSoup(str(next), 'lxml')
    #     content = reg1.sub('', next_soup.prettify()).split('\n')
    #     content = ''.join(content)
    #     if len(content) > 30:
    #         msg.append(''.join(content))
    #         msg_len.append(len(msg))
    # parent = title.parent
    # next_soup = BeautifulSoup(str(parent), 'lxml')
    # content = reg1.sub('', next_soup.prettify()).split('\n')
    # print ''.join(content)
    # next = parent.next_sibling
    # while next != None:
    #     next = next.next_sibling
    #     if len(str(next)) < 30:
    #         continue
    #     next_soup = BeautifulSoup(str(next), 'lxml')
    #     content = reg1.sub('', next_soup.prettify()).split('\n')
    #     for c in content:
    #         if len(c.strip())==0:
    #             continue
    #         print str(len(c.strip()))+" "+c

    # soup2 = BeautifulSoup(str(text), 'lxml')
    # reg1 = re.compile("<[^>]*>")
    # content = reg1.sub('', soup2.prettify()).split('\n')
    # print ''.join(content)



#获取编码类型
def getcodetype(html):
    soup = BeautifulSoup(html, 'lxml')
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


if __name__ == '__main__':
    text  =getcontentfromweb('http://news_and_blog.qq.com/a/20170619/002792.htm')
    parser(text)