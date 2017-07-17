# coding: utf8

# @Author: 郭 璞
# @File: Main.py                                                                 
# @Time: 2017/4/28                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: The entrance of this blog backup tool.

from csdnbackup.login import Login
from csdnbackup.backup import Backup
from csdnbackup.blogscan import BlogScanner
import random
import time
import getpass

username = input('请输入账户名：')
password = getpass.getpass(prompt='请输入密码：')


loginer = Login(username=username, password=password)
session = loginer.login()

scanner = BlogScanner(username)
links = scanner.scan()

for link in links:
    print("开始备份：{}".format(link))
    timefeed = random.choice([1,2,3,4,5,6,7])
    time.sleep(timefeed)
    print('随即休眠{}秒'.format(timefeed))
    backupper = Backup(session=session, backupurl=link)
    backupper.backup(outputpath='./hanlu')
