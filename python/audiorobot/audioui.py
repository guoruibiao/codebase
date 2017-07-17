# coding: utf8

# @Author: 郭 璞
# @File: audioui.py                                                                 
# @Time: 2017/5/11                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 外部界面
from PyQt5 import QtCore, QtGui, QtWidgets
from audiorobot.dispatcher import Dispatcher
from audiorobot.baiduyuyin import BaiDuYuYin
from audiorobot.turing import TuringRobot
from audiorobot.localvoicer import Speaker

class ClientUI(QtWidgets.QWidget):

    def __init__(self):
        super(ClientUI, self).__init__()
        self.dispatcher = Dispatcher()
        self.baiduyuyin = BaiDuYuYin()
        self.turingrobot = TuringRobot()
        self.speaker = Speaker()
        self.initui()


    def initui(self):
        self.setWindowTitle("图灵·聊天室")
        self.setGeometry(20, 20, 400, 500)

        # 顶部布局
        toplayout = QtWidgets.QHBoxLayout()
        self.textarea = QtWidgets.QTextBrowser()
        toplayout.addWidget(self.textarea)
        # 中间布局
        centerlayut = QtWidgets.QHBoxLayout()
        self.editline = QtWidgets.QLineEdit()
        self.voicebutton = QtWidgets.QPushButton("发语音")
        self.textbutton = QtWidgets.QPushButton("发文字")
        centerlayut.addWidget(self.editline)
        centerlayut.addWidget(self.voicebutton)
        centerlayut.addWidget(self.textbutton)

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(toplayout)
        mainlayout.addLayout(centerlayut)

        self.setLayout(mainlayout)
        # 关于事件处理，交给handler来处理即可
        self.eventhandler()

    def eventhandler(self):
        self.voicebutton.clicked.connect(self.pushvoice)
        self.textbutton.clicked.connect(self.pushtext)

    def pushvoice(self):
        print('voice')
        # 先保存到本地，再调用语音接口上传
        self.dispatcher.record()
        response = self.baiduyuyin.parse()
        print('百度语音接口解析到的数据为：{}'.format(response))
        self.speaker.speak(text=response)
        # 更新一下窗体文本域的内容
        text = self.textarea.toPlainText()+"\n"+"<<< "+"上传音频中..."
        self.textarea.setText(text)
        text =  text +"\n>>> " +response
        self.textarea.setText(text)


    def pushtext(self):
        inputtext = self.editline.text()
        print(inputtext)
        trans = self.turingrobot.talk(text=inputtext)
        self.speaker.speak(text=trans)
        # 更新文本域内容
        text = self.textarea.toPlainText() + "\n<<<"+inputtext
        self.textarea.setText(text)
        text = self.textarea.toPlainText() + "\n>>> " + trans
        self.textarea.setText(text)
        self.editline.clear()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ClientUI()
    ui.show()
    sys.exit(app.exec_())
