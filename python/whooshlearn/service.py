# coding: utf8

# @Author: 郭 璞
# @File: service.py                                                                 
# @Time: 2017/5/13                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 通过flask整合搜索服务

from flask import Flask, request
import hashlib
from whooshlearn.db import dbhelper
from whooshlearn.csdn import *

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def search():
    username = request.form['username']
    token = request.form['token']
    querystring = request.form['query']

    helper = dbhelper()
    searcher = Searcher()
    usertoken = helper.gettoken(username)

    # 开始验证返回的token是否为已配备的
    # if token == helper.gettoken(username=username):
    if token == usertoken:
        # # 开始服务
        prehandle(username=username)
        result = searcher.search(querystring)
        print(result)
        return "<code>{}</code>".format(result)
    else:
        # 给出合理的解释
        return "<h2>抱歉您没有权限被服务，请联系博主。</h2><br><a href='http://blog.csdn.net/marksinoberg'>博客地址</a>"


def prehandle(username):
    session = Login().login(username='1064319632@qq.com', password='PRCstylewarmup')
    blogs = BlogScanner(domain=username).scan()
    searcher = Searcher()
    for item in blogs[0:7]:
        print("正在处理文章：{}".format(item))
        blogdetails = BlogDetails(session=session, blogurl=item).getSource()
        searcher.addblog(blogdetails)

@app.route("/user/register", methods=["POST", "GET"])
def register():
    username = request.form['username']
    token = hashlib.md5(username.encode('utf8')).hexdigest()
    # 保存到数据库中之前先检查一下对应名称的username是否已经被注册
    info = {
        'username': username,
        'token': token,
    }
    helper = dbhelper()
    helper.add(info=info)
    return "<h2>Congratulations for your register.</h2><br>Your token is: {} please use it for your searching service!".format(token)


if __name__ == '__main__':
    app.run(host="localhost", port=8888, debug=True)