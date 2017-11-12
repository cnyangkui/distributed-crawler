# -*- encoding: utf-8 -*-
from geospider.news_and_blog.article_parser import *
from bs4 import BeautifulSoup

def get_article_node(lines):
    soup = BeautifulSoup(''.join(lines), 'lxml')
    title_node = soup.title
    if title_node == None:
        return None
    title = title_node.text.strip()
    h1_node = soup.h1
    if h1_node == None:
        return None
    h1 = h1_node.text.strip()
    if h1 not in title:
        return None
    node = traversal_brother(h1_node)
    if node==None:
        node=h1_node
    print(node.text)
    while len(node.text) < 300 and node!=None and node.name!=None:
        node = traversal_parent(node)
    nodes = []
    msg_len = []
    while node!=None:
        nodes.append(node)
        msg_len.append(len(get_tag_text(node)))
        node = traversal_children(node)
    msg_size = len(msg_len)
    aipha = 0.6
    for i in range(0, msg_size-1):
        if msg_len[i+1]  < msg_len[i]*aipha:
            return nodes[i]
    return None

def traversal_parent(node):
    parent_node = node.parent
    if parent_node==None:
        return None
    return traversal_brother(parent_node)

def traversal_children(node):
    children = node.contents
    children_len = len(children)
    nodes = []
    msg_len = []
    node_num =0
    for i in range(0, children_len):
        if children[i].name!=None:
            line = get_tag_text(children[i])
            nodes.append(children[i])
            msg_len.append(len(line))
            node_num+=1
    if node_num ==0:
        return None
    max_index = msg_len.index(max(msg_len))
    return nodes[max_index]

def traversal_brother(node):
    nodes = []
    msg_len = []
    next = node.next_sibling
    node_num=0
    while next!=None and next.name!=None:
        line = get_tag_text(next)
        # print(str(len(line)) + " " + line)
        nodes.append(next)
        msg_len.append(len(line))
        next = next.next_sibling
        node_num+=1
    if node_num==0:
        return None
    max_index = msg_len.index(max(msg_len))
    return nodes[max_index]

def get_tag_text(node):
    text = re.sub("\\s+", '', node.text)
    return text

if __name__ == '__main__':
    url = "http://news_and_blog.qq.com/a/20170619/019941.htm"
    html = get_html(url)
    lines = filter_tags(html, False)
    article_node = get_article_node(lines)
    print(article_node)
    # article = get_tag_text(article_node)
    # print(article)