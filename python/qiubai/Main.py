# coding: utf8

# @Author: 郭 璞
# @File: Main.py                                                                 
# @Time: 2017/4/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 糗事百科 带界面版本

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

def getdata(page=3):
    """
    实时获取糗事百科段子，默认页数为3，可进行外部控制。但是范围是1-35.
    :param page:
    :return:
    """
    if page <1 or page > 35:
        raise Exception('您输入的页码超过了官网限制！请保持在1-35之间！')
    else:
        total = []
        for index in range(page):
            url = 'http://www.qiushibaike.com/8hr/page/{}/'.format(index + 1)
            result = show(url=url)
            total.extend(result)
        # 返回获取到的段子字典，以供外部调用！
        return total

def ui(title="糗事百科段子--桌面版"):
    global label
    root = Tk()
    root.title(title)
    label = Label(root, text="系统正在努力为您拉取段子\n请稍后... ...", height=36, compound='center')
    label['text'] = "软件使用方法：\n- 按方向键←或者↑查看上一条段子\n- 按方向键↓或者→查看下一条段子。\n系统正在努力为您拉取段子\n请稍后... ..."
    label.pack()
    root.bind_all('<KeyPress>', eventhandler)
    root.mainloop()

def eventhandler(event):
    global index
    total = getdata(page=3)
    index = (index+len(total))%len(total)
    if event.keysym == 'Up' or event.keysym == "Left":
        index -= 1
        print('前一个')
    elif event.keysym == 'Down' or event.keysym == 'Right':
        index += 1
        print('下一个')

    content = "发帖人：\t{}\n".format(total[index]['username'])+"\n\t{}\n".format(total[index]['content'])+"热评：{}\n".format(total[index]['hotcomment'])
    label['text'] = content

if __name__ == '__main__':
    content = ""
    index = 0
    label = None
    ui(title='我的糗事百科桌面版')
