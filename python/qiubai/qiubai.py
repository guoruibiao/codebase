# coding: utf8

# @Author: 郭 璞
# @File: qiubai.py                                                                 
# @Time: 2017/4/14                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 糗事百科段子，及热评。http://www.qiushibaike.com/

# 网络操作相关
import requests
from bs4 import BeautifulSoup
# 创建一个接口，返回json串
import json

# 创建GUI使用
from tkinter import *

def show(url):
    headers = {
        'host':'www.qiushibaike.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    response = None
    containers = soup.find_all('div', {'class': 'article block untagged mb15'})
    result = []

    for container in containers:
        # 'div', {'class': 'author clearfix'}
        try:
            # 对于非匿名用户可正常获取
            username = container.find('div', {'class': 'author clearfix'}).find_all('a')[1].find('h2').get_text()
        except:
            # 对于匿名用户，HTML标签特殊处理
            username = container.find('div', {'class': 'author clearfix'}).find_all('span')[1].get_text()
        # print(username)
        content = container.find('a', {'class': 'contentHerf'}).find('div', {'class': 'content'}).find('span').get_text()
        # print(content)
        try:
            hotcommentuser = container.find('a', {'class': 'indexGodCmt'}).find('div', {'class': 'cmtMain'}).find('span', {'class': 'cmt-name'}).get_text()
            hotcommentcontent = container.find('a', {'class': 'indexGodCmt'}).find('div', {'class': 'cmtMain'}).find('div', {'class': 'main-text'}).get_text()
            # 去除大块大块的空格，尽量去掉换行标记。
            hotcomment = str(hotcommentuser).strip(' ').strip('\n').strip('\r') + str(hotcommentcontent).strip(' ').strip('\n').strip('\r')
        except:
            # 奇奇怪怪的问题。
            hotcomment = "热评人： 无， 热评内容： 无"

        # 封装糗事及评论
        item = {
            'username': username,
            'content': content,
            'hotcomment': hotcomment
        }
        result.append(item)

    # 以列表的形式返回数据，以备调用
    return result

def api(page=3):
    total = []
    for index in range(page):
        url = 'http://www.qiushibaike.com/8hr/page/{}/'.format(index + 1)
        result = show(url=url)
        total.extend(result)
    return json.dumps(total)

def main(page=3, outputpath='./qiubai.txt'):
    """
    想要获取几页的数据啊
    :param page:
    :return:
    """
    total = []
    for index in range(page):
        url = 'http://www.qiushibaike.com/8hr/page/{}/'.format(index+1)
        result = show(url=url)
        total.extend(result)
    # 待会可以删除，转为json格式罢了
    total = json.dumps(total)
    # 写入一个文件待用
    with open(outputpath, 'a', encoding='utf8') as f:
        for item in total:
            f.write(str(item)+"\n")
        f.close()
    print('糗事百科笑话全部入库，详情请查看{}文件'.format(outputpath))

################################################################################



def ui(list):
    root = Tk()
    root.title('糗事百科')
    root.geometry("500x390")
    root.resizable(width=False, height=False)
    # 设置显示标签
    text = Text(root)
    text.insert(END, 'dadasdassad')
    text.pack()
    # 设置一个内部函数
    def change(list, index):
        """
        index 为向前向后移动的方向。1向后，-1向前
        :param list:
        :param index:
        :return:
        """
        text.delete(1.0, END)
        text.insert(END, list[3])
        print(index)
    # 设置按钮
    Button(root, text="上一个", command=change(list, -1)).pack()
    Button(root, text="下一个", command=change(list, 1)).pack()
    root.mainloop()




if __name__ == '__main__':
    # 官网最大上限为35页
    main(page=3, outputpath=r'c:\users\biao\Desktop\qiubai.json')
    # json = api(page=1)
    # print(json)