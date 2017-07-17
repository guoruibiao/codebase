# coding: utf8

# @Author: 郭 璞
# @File: localvoicer.py                                                                 
# @Time: 2017/5/11                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 本地语音朗读实现。
import win32com.client

class Reader(object):
    """
    尴尬的是pyttsx不支持Python36，要不然还可以有更多可选项。
    """

    def __init__(self):
        import pyttsx
        self.engine = pyttsx.init()
        # optional property
        self.rate = self.engine.getProperty('rate')
        self.voices = self.engine.getProperty('voices')
        self.volume = self.engine.getProperty('volume')

    def read(self, text="", rate=200, voices="", volume=""):
        self.engine.say(text)
        self.engine.runAndWait()


class Speaker(object):
    def __init__(self):
        self.engine = win32com.client.Dispatch("SAPI.SpVoice")

    def speak(self, text):
        self.engine.Speak(text)



if __name__ == '__main__':
    # reader = Reader()
    # reader.read(text='Hello World!')
    speaker = Speaker()
    speaker.speak("hello world! 你好世界")

