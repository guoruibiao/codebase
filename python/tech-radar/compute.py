#!usr/bin/env python
# coding: utf8
import requests
import math
import re
from bs4 import BeautifulSoup


class Radar(object):
    """
    技术雷达实现
    """

    def __init__(self, username):
        """初始化用户名以及相应的域名前缀"""
        self.username = username
        self.domain = "http://blog.csdn.net"

    def download(self, url):
        """下载通用方法"""
        headers = {
            'Host': 'blog.csdn.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        return response.text if response.status_code == 200 else None

    def str_concat(self, *args):
        """ 字符串拼接方法，满足不定参数的实现"""
        tempstr = ''
        for item in args:
            tempstr += item
        return tempstr

    def get_catagories(self):
        """
        计算username对应的文章类别信息，获取类别名称， 对应的URL以及为其设置编号
        """
        url = self.str_concat(self.domain, '/', self.username)
        html = self.download(url=url)
        soup = BeautifulSoup(html, 'html.parser')
        temp_catagories = soup.find_all('div', {'id': 'panel_Category'})[-1].find_all('a')
        catagory = []
        for index, item in enumerate(temp_catagories):
            counts = soup.find_all('div', {'id': 'panel_Category'})[-1].find_all('span')[index+1].get_text().lstrip('(').rstrip(')')
            obj = {
                "url": self.str_concat(self.domain, item.attrs['href']),
                "name": item.get_text(),
                "counts": int(counts)
            }
            catagory.append(obj)
        # 返回类别相关的计算结果
        return catagory

    def trim_list(self, ls):
        """
        列表去重
        """
        return list(set(ls))

    def get_posts(self, catagory_url, counts):
        """
        根据给定的类别URL，获取该类别下所有的文章的链接以及标题信息等
        """
        html = self.download(url=catagory_url)
        # 先使用正则来获取给类别对应的文章总数，以及总页数
        posts_number, pages = counts, math.ceil(counts/20)
        html = None
        # 声明一个保存文章信息的容器列表
        posts = []
        # 对每一页的链接进行爬取，获取对应页面文章的标题以及链接  int(pages)+1
        for index in range(1, int(pages) + 1):
            # print("正在处理第{}页".format(index))
            url = self.str_concat(catagory_url, '/', str(index))
            html = self.download(url=url)
            soup = BeautifulSoup(html, 'html.parser')
            page_posts = soup.find_all('span', {'class': 'link_title'})
            for item in page_posts:
                url = re.findall(re.compile('href="(.*?)"'), str(item))
                if(url == []):
                    continue
                posts.append(self.str_concat(self.domain, url[0]))
            # print("第{}页的数据为：{}个".format(index, len(page_posts)))
        return self.trim_list(posts)

    def get_detail(self, posturl):
        """
        根据指定的博文URL链接，计算出改文章大致的得分情况。
        默认按照CSDN官方计算规则实现。
        每300浏览量加一分；一个赞加一分；一个评论加一分；一个踩扣一分
        """
        html = self.download(url=posturl)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('span', {'class': 'link_title'}).get_text()
        watches = re.findall(re.compile('.*?(\d+).*?'), soup.find('span',{'class': "link_view"}).get_text())[0]
        comments = re.findall(re.compile('.*?\((\d+)\).*?'), soup.find('span',{'class': "link_comments"}).get_text())[0]
        diggs = soup.find('dl', {'id': 'btnDigg'}).find('dd').get_text()
        buries = soup.find('dl', {'id': 'btnBury'}).find('dd').get_text()
        # 简单 计算出每篇文章的得分情况
        print('正在计算 {} 的得分情况。'.format(posturl))
        return int(watches)/300+int(comments)+int(diggs)-int(buries)
