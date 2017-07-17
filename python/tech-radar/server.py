#!/usr/bin/env python
# coding: utf8
import json
from utils import compute
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/api/user/<username>', methods=['GET', 'POST'])
def get_user_score(username):
    catagories = compute(username=username)
    return json.dumps(catagories)


@app.route('/')
def home():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(host='localhost', port=8888, debug=True)
