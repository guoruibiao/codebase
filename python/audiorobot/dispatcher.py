# coding: utf8

# @Author: 郭 璞
# @File: dispatcher.py
# @Time: 2017/5/11
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 业务管家，处理本地音频记录上传，并读取网络返回文本数据流

from audiorobot import baiduyuyin, localvoicer, recorder
# from audiorobot import audioui
# from PyQt5 import QtWidgets, QtGui
# import sys


class Dispatcher(object):

    def __init__(self):
        self.yuyinclient = baiduyuyin.BaiDuYuYin()
        self.speaker = localvoicer.Speaker()
        self.recorder = recorder.Recorder()

    def speak(self, text=""):
        # 获取语音数据
        texts = self.yuyinclient.parse()
        for item in texts:
            self.speaker.speak(text=item)

    def record(self):
        self.recorder.record()


# #-------------------------------
# class MyWindow(audioui.ClientUI):
#     def __init__(self):
#         super(MyWindow, self).__init__()
#
#
#
#
#
# if __name__ == '__main__':
#     # pass
#     # dispatcher = Dispatcher()
#     # dispatcher.speak()
#     # dispatcher.record()
#     app = QtWidgets.QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     sys.exit(app.exec_())


