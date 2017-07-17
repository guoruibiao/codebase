# coding: utf8

# @Author: 郭 璞
# @File: tkusage.py                                                                 
# @Time: 2017/4/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 使用Tkinter创建一个布局

from tkinter import *
import random

# root = Tk()
# root.title('窗口测试')

label = None

content = ""

def ui(root):
    global label
    global content
    label = Label(root, text="这里将显示内容部分", width=66, height=28, compound="center")
    prebtn = Button(root, text="上一个", width=19, bg='red', compound="left", relief='raised', command=btn_callback)
    nextbtn = Button(root, text='下一个', width=19, compound='right', command=btn_callback)
    # 绑定键盘事件
    prebtn.bind('<Left>', eventhandler)
    nextbtn.bind('<Right>', eventhandler)
    root.focus_set()
    label.pack()
    prebtn.pack()
    nextbtn.pack()

def eventhandler(event):
    print('按下了字符{}'.format(event.char))
    print('按下的键值为：{}'.format(event.keycode))

def btn_callback():
    label['text'] = """
    Username: Mark\n
    正文：
        哈哈哈哈哈哈
    \n
    热评：
        热评人： 赵六。 热评内容： 老铁， 666
    """

    print("Hello Tkinter!")


if __name__ == '__main__':
    root = Tk()
    root.title("窗口测试")
    ui(root=root)
    root.mainloop()
