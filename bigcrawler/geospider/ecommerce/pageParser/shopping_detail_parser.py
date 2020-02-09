# -*-encoding:utf-8 -*-

import re
import requests
from geospider.ecommerce.spiderUtils.parser_util import get_soup_by_request,get_soup_by_selenium,get_webdriver,get_soup_by_html_source
from geospider.ecommerce.spiderUtils.url_utils import pic_url_sifter

import sys

reload(sys)
sys.setdefaultencoding('utf8')


def _get_price_in_script(soup):
    # print soup.prettify()
    script_list = soup.find_all('script')
    re_str = '"price\w*":"\d+\.\d{1,3}"'
    re_digit_str = "\d+\.\d{1,3}"
    for each_script in script_list:
        res = re.search(re_str,str(each_script))
        if(res!=None):
            # print res.group()
            return re.search(re_digit_str,res.group()).group()


def _get_price_by_class(soup,class_name):
    res_price_list = []
    reg_without_keyword = "\d+\.\d{1,3}"

    tag_symbol_list = soup.find_all(True, class_=re.compile(class_name))
    for tag in tag_symbol_list:
        tag_tmp = tag
        price_text_list = []
        attemps = 0
        while (len(price_text_list) == 0 and attemps < 2):
            price_text_list = re.findall(reg_without_keyword, tag_tmp.text)
            tag_tmp = tag_tmp.parent
            attemps += 1

        # print res_price_list
        if (len(price_text_list) != 0):
            res_price_list = res_price_list + price_text_list

    return res_price_list

def _get_price_by_keyword(soup,keyword):
    res_price_list = []
    reg_with_keyword = u"%s\s*\d+\.*\d{1,3}"%keyword

    reg_digit_keyword = u"\d+\.\d{1,3}" #从带有关键字的字符串中提取价格（数字），例如促销价 100,则提取出100


    ttt = u'%s'%keyword
    tag_symbol_list = soup.find_all(True, text=re.compile(ttt))
    # print '%s,%s'%(keyword,str(tag_symbol_list))


    for tag in tag_symbol_list:
        for s_tag in tag.parent.contents:
            # print (s_tag)
            try:
                one_price =  re.search(reg_digit_keyword,str(s_tag)).group()
                res_price_list.append(one_price)
            except:
                # print "shopping_detail_parser.py  error"
                pass

    # for tag in tag_symbol_list:
    #     ss = str(tag.parent.parent)
    #     # print ss
    #     soup_tmp = get_soup_by_html_source(ss)
    #     print soup.find_all('img')


    price_dic = {}
    max_appear_price = "-1"
    max_appear_price_num = -1

    for each_price in res_price_list:
        if (price_dic.has_key(each_price)):
            price_dic[each_price] += 1
        else:
            price_dic[each_price] = 1
        if (price_dic[each_price] > max_appear_price_num):
            max_appear_price_num = price_dic[each_price]
            max_appear_price = each_price

    # print max_appear_price
    return max_appear_price

def _get_store_by_key(soup,keyword,url):

    def not_empty(s):
        return s and s.strip()

    # json_key_list = list(filter(not_empty, max_path_str.split('/')))

    tag_symbol_list = soup.find_all("a", text=re.compile(keyword))
    res_stroe_dict = {}
    stroe_comments = []
    for tag in tag_symbol_list:
        try:
            stroe_url = tag['href']
            res_stroe_dict['store_url'] = stroe_url

            # tag_contents
            if('tmall' in url):
                tag_contents = tag.parent.parent.parent.parent.parent.contents
            else:
                tag_contents = tag.parent.parent.parent.parent.contents

            for inner_stroe_tag in  tag_contents:
                if inner_stroe_tag.name !=None:


                    store_m =  (inner_stroe_tag.text.replace(" ",""))
                    store_m_list =  (list(filter(not_empty, store_m.split('\n'))))
                    store_m_len = len(store_m_list)
                    # print '\n'.join(store_m_list)
                    index = 0
                    for index in range(0,store_m_len):
                        message = store_m_list[index]
                        if(index == 0):
                            # print "店铺名：%s"%message
                            res_stroe_dict['name'] = message
                        else:
                            re_res = re.search('\d+\.\d+',str(message))
                            if(re_res != None and re.search('\d+\.\d+',str(store_m_list[index-1]))==None):
                                # print ("%s：%s"%(store_m_list[index-1],store_m_list[index]))
                                stroe_comments.append("%s:%s"%(store_m_list[index-1],store_m_list[index]))
            res_stroe_dict['comment_degree'] = ';'.join(stroe_comments)
            # print  res_stroe_dict['comment_degree']
        except:
            pass

    return res_stroe_dict
    #     print res_price_list
    #     if (len(price_text_list) != 0):
    #         res_price_list = res_price_list + re.findall(reg_without_keyword, "".join(price_text_list))
    #
    # return res_price_list
def get_price(soup):
    # soup = get_soup_by_request(url)
    # print soup.prettify()
    price_keys = [u"¥",u"促销价",u"价格",u"价"]
    for keyword in price_keys:
        res = _get_price_by_keyword(soup, keyword)
        if(res !=None and res !=[] and res != "-1"):
            # print res
            return res


    res_price_list = _get_price_by_class(soup, "price.*")
    if (len(res_price_list) != 0):
        return res_price_list

    _get_price_in_script(soup)

    res = _get_price_in_script(soup)
    return res
# def _get_comments_by_keyword(soup,keyword):


def get_comments(soup):



    # req = requests.get(url)
    # req.encoding = "utf-8"
    # doc = etree.HTML(driver.page_source)
    key = u"评论"
    # print  doc.xpath("//*[text()='%s']"%(key))
    driver = get_webdriver()
    driver.get(url)
    # soup = BeautifulSoup(driver.page_source,'lxml')
    # print driver.page_source
    # print soup.prettify()
    # for y in soup.find_all(True,text=re.compile(key)):
    #     for x in y.parent.parent.children:
    #         print x
    # driver = get_webdriver(url)
    # driver.get(url)
    xxx = driver.find_element_by_xpath('//*[contains(text(),"%s")]' % key)

    # print  xxx.text
    # print  xxx.tag
    driver.close()



def get_store(soup,url):

    soup = get_soup_by_request(url)

    store_keys = [u'旗舰店',u'进入店',u'店铺',u'进店',u'店']
    for keyword in store_keys:
        res_dict = _get_store_by_key(soup, keyword,url)
        if(res_dict !=None and res_dict!={} and res_dict.has_key('store_url')):
            # print res_dict
            return res_dict
        # print res_url
        # if(res_url !=None and res_url !=[]):
        #     test_url =  url_sifter(url,res_url)
        #     print get_soup_by_request(test_url).find('title').text
        #     return url_sifter(url,res_url)
    return None

def get_pic_url(soup,url):
    img_list = soup.find_all('img')
    regular = r'\d{3,}x\d{3,}'
    max_pic_size = -1
    max_pic_url= ""
    img_url_set = set()
    for im in img_list:
        try:
            pic_url = pic_url_sifter(url, im['src'])
            if (pic_url != None and ('jpg' in pic_url or 'png' in pic_url or 'jpeg' in pic_url)):
                img_url_set.add(pic_url)
                re_res =  re.search(regular,pic_url).group()
                re_res_splited = re_res.split('x')
                pic_size = max(int(re_res_splited[0]),int(re_res_splited[1]))

                if(pic_size > max_pic_size):
                    max_pic_size = pic_size
                    max_pic_url = pic_url
        except:
            pass

    print max_pic_url
    if(max_pic_size != -1):
        return max_pic_url


    max_len = -1
    res_pic_url = ""
    pic_set = set()
    for pic_url in img_url_set:
        try:
            if(pic_url in pic_set):
                continue
            else:pic_set.add(pic_url)

            pic_len = len(requests.get(pic_url).text)
            if(pic_len > max_len):
                max_len = pic_len
                res_pic_url = pic_url
        except:
            pass

    return res_pic_url


def get_title(url):
    soup = get_soup_by_request(url)
    tag_script = soup.find("title")
    return tag_script.text

def get_comment_degree(url):
    key = u"好评"

def get_goods_dict_without_stroe(url):
    soup = get_soup_by_request(url)
    res_dict = {}

    res_dict['title'] = soup.find("title").text
    res_dict['price'] = get_price(soup)
    res_dict['pic_url'] = get_pic_url(soup, url)
    res_dict['detail_url'] = url

    return res_dict


def get_goods_dict(url):
    soup = get_soup_by_request(url)
    res_dict = {}

    res_dict['title'] = soup.find("title").text
    res_dict['price'] = get_price(soup)
    res_dict['pic_url'] = get_pic_url(soup,url)
    res_dict['detail_url'] = url

    store_dict =  get_store(soup,url)
    if(store_dict !=None and store_dict.has_key('comment_degree') and 'dangdang.com' not in url):
        res_dict['comment_degree'] = store_dict['comment_degree']
    else:
        res_dict['comment_degree'] = ""

    return res_dict
if __name__ == '__main__':
    # url = "https://detail.tmall.com/item.htm?spm=a230r.1.14.14.AT6RIa&id=544429684821&cm_id=140105335569ed55e27b&abbucket=20"
    # url = "https://item.taobao.com/item.htm?spm=a230r.1.14.97.oI9e6K&id=545728190154&ns=1&abbucket=20#detail"
    # url = "https://item.jd.com/11225370508.html"
    # url = "http://item.meilishuo.com/detail/1kaosga?acm=3.ms.2_4_1kaosga.0.24476-25176.94mOaqibAUDJd.t_0-lc_3&ptp=1.9Hyayb.classsearch_mls_1kaosga_2017%E6%96%B0%E6%AC%BE%E6%AC%A2%E4%B9%90%E9%A2%82%E7%8E%8B%E5%AD%90%E6%96%87%E6%9B%B2%E7%AD%B1%E7%BB%A1%E5%90%8C%E6%AC%BE%E5%8C%85%E6%97%B6%E5%B0%9A%E5%B0%8F%E6%96%B9%E5%8C%85%E5%8D%95%E8%82%A9%E6%96%9C%E6%8C%8E%E5%B0%8F%E5%8C%85%E5%8C%85_10057053_pop.1.mNWwi"
    # url = "http://shop.mogujie.com/detail/18jws1w?acm=3.ms.1_4_18jws1w.43.1185-22922.wGTRPqnDRVaKO.t_0-lc_4&ptp=1.eW5XD._b_4bce2add492e4c56_2.1.DijfM"
    url = 'http://product.dangdang.com/23512622.html'
    # get_comments(url)


    print get_price(get_soup_by_request((url)))
    # get_store(get_soup_by_request(url),url)
    # get_title(url)
    # get_pic_url(url)

