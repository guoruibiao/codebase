# coding: utf8

# @Author: 郭 璞
# @File: turing.py
# @Time: 2017/5/11                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 文字对话接口实现
import requests
import json

class TuringRobot(object):

    def __init__(self):
        self.apikey = '2a220b38970844309f6503db51674c54'
        self.userid = '1357924680'
        self.url = 'http://www.tuling123.com/openapi/api'

    def talk(self, text):
        payload = {
            'key': self.apikey,
            'userid': self.userid,
            'info': text
        }

        response = requests.post(url=self.url, data=payload)
        return json.loads(response.text)['text']


if __name__ == '__main__':
    turing = TuringRobot()
    answer = turing.talk('你好吗，我是小黄鸡！')
    print(answer)