# coding: utf8

# @Author: 郭 璞
# @File: platform.py                                                                 
# @Time: 2017/4/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 

from tkinter import *

platform = Tk()
platform.title('标题部分')
Label(platform, text='Username:').pack(side=LEFT)
Entry(platform, bg='black', fg='white', width=12).pack(side=LEFT)


platform.mainloop()
