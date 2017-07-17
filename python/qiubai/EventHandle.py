# coding: utf8

# @Author: 郭 璞
# @File: EventHandle.py                                                                 
# @Time: 2017/4/21                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 处理事件响应

from tkinter import *

root = Tk()

root.title("窗口测试")

def eventhandler(event):
    print("按下了：", event)

root.bind_all('<Enter>', eventhandler)

root.mainloop()

# Cancel/Break/BackSpace/Tab/Return/Sift_L/Shift_R/Control_L/Control_R/Alt_L/Alt_R/Pause
#        Caps_Loack/Escape/Prior(Page Up)/Next(Page Down)/End/Home/Left/Up/Right/Down/Print/Insert/Delete/
#        F1-12/Num_Lock/Scroll_Lock