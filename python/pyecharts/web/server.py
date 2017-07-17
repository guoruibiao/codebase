# coding: utf8

# @Author: 郭 璞
# @File: server.py                                                                 
# @Time: 2017/6/23                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 利用Flask启用一个本地web服务，为echarts提供后台支持。
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    return "<h2>It Works.</h2>"


@app.route('/api/charts/<chartname>', methods=['GET', 'POST'])
def charts(chartname):
    from pyecharts.core.simple import make_data
    if chartname == 'radar':
        return make_data()
    else:
        return make_data()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='localhost', port=8888, debug=True)

