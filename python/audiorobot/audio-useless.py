# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'audio.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class MyButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(MyButton, self).__init__(parent)
        self.setStyleSheet('''background-color:purple;''')

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # 传递至父窗口响应鼠标按下事件
            self.parent().mousePressEvent(event)


class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(452, 511)
        # 申请一个状态条信息
        # self.statusBar()

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 431, 391))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 419, 431, 73))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.pushButton_2 = MyButton()
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        # 将事件处理交给专门的处理方法
        self.eventhandler()
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "发语音"))
        self.pushButton.setText(_translate("Form", "发文字"))

        

    def eventhandler(self):
        # 处理信号和槽
        # 发布文字相关处理
        self.pushButton.clicked.connect(self.pushtext)
        # 发布语音相关处理
        self.pushButton_2.clicked.connect(self.pushvoice)



    def pushvoice(self):
        self.statusBar().showMessage("正在录音...")
        # import time
        # time.sleep(3)
        print('发送了语音，内容为：{}'.Format(self.textEdit.toPlainText()))
        self.statusBar().showMessage("录音完毕！")

    def pushtext(self):
        print('发送了文字，内容为：{}'.Format(self.textEdit.toHtml()))
        text = self.textBrowser.toHtml() + self.textEdit.toHtml()
        self.textBrowser.setText(text)

