# coding: utf8

# @Author: 郭 璞
# @File: db.py                                                                 
# @Time: 2017/5/13                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 用于存储注册用户的一些信息。username和token权限
import sqlite3

class dbhelper(object):

    def __init__(self):
        self.db = "userinfo.db"


    def add(self, info={}):
        username = info['username']
        token = info['token']
        sql = "insert into user(username, token) values('{username}', '{token}')".format(username=username, toekn=token)
        conn = sqlite3.connect(self.db, timeout=7)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def isduplicate(self, username):
        sql = "select count(*) from user where username='{}'".format(username)
        conn = sqlite3.connect(self.db, timeout=7)
        cursor = conn.cursor()
        cursor.execute(sql)
        number = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        if number == 1:
            return True
        else:
            return False

    def gettoken(self, username):
        flag = self.isduplicate(username=username)
        if flag:
            conn = sqlite3.connect(self.db, timeout=7)
            cursor = conn.cursor()
            sql = "select token from user where username='{}'".format(username)
            cursor.execute(sql)
            token = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return token
        else:
            raise Exception("{} not registered!".format(username))


#
# if __name__ == '__main__':
#     helper = dbhelper()
#     token = helper.gettoken(username='marksinoberg')
#     print(token)



# conn = sqlite3.connect('userinfo.db')
# cursor = conn.cursor()


# sql = """
# create table user(
#     id integer primary key,
#     username varchar(36) UNIQUE not NULL ,
#     token VARCHAR(128) not NULL
#     );
# """
# cursor.execute(sql)
# conn.commit()
#
# cursor.execute("select * from user")
#
# print(cursor.fetchall())

# sql = "select count(*) from user where username='{}'".format('asdbadsa')
# cursor.execute(sql)
# print(cursor.fetchone()[0])
# cursor.close()
