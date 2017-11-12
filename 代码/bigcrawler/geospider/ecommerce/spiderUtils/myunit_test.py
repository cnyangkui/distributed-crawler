# coding:utf-8
# from selenium import webdriver
# import  time
# url = "http://category.vip.com/"
# driver  = webdriver.PhantomJS()
# driver.get(url)
# # time.sleep(5)
# print driver.page_source
import requests

resq = requests.get("http://www.dangdang.com/")
resq.encoding = "gb2312"
print resq.text