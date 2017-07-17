# coding: utf8

# @Author: 郭 璞
# @File: spider.py                                                                 
# @Time: 2017/6/23                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 抓取图标，并将图片显示到本地。

import requests
from selenium import webdriver
import base64

url = 'http://localhost:8888'

browser = webdriver.Chrome()
browser.get(url)

browser.find_element_by_id("compute").click()
print(browser)
import time
print('休眠10秒')
time.sleep(10)

data = browser.find_element_by_id('target').click()
print('图片下载完成.')

path = r'C:\Users\biao\Downloads\下载.png'
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

lena = mpimg.imread(path)
plt.imshow(lena)
plt.axis('off')
plt.show()