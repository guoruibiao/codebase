# coding: utf8

# @Author: 郭 璞
# @File: simple.py                                                                 
# @Time: 2017/6/23                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 临时测试
import json

def make_data():
    data = [{"name": name, "score": score} for name, score in [('a', 12), ('b', 3), ('c', 34), ('d', 15), ('e', 66), ('f', 7)]]
    return json.dumps(data)

