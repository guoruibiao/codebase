# coding: utf8

# @Author: 郭 璞
# @File: test.py                                                                 
# @Time: 2017/4/28                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 关于CSDN 博客备份的所有测试相关临时数据
from csdnbackup.login import Login
from csdnbackup.backup import Backup
from csdnbackup.blogscan import BlogScanner


# loginer = Login(username='marksinoberg', password='PRCstylewarmup')
# session = loginer.login()
# # print(session.cookies)
#
# modifyurl = 'http://blog.csdn.net/marksinoberg/article/details/70432419'
# backupper = Backup(session=session, backupurl=modifyurl)
# # loginer.getSource(url=modifyurl)
# source = backupper.getSource()
# print(source)
# pics = backupper.getpicurls()
# backupper.backup(outputpath='./')

scanner = BlogScanner('marksinoberg')
links = scanner.scan()
print(len(links))