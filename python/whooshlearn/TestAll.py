# coding: utf8

# @Author: 郭 璞
# @File: TestAll.py                                                                 
# @Time: 2017/5/12                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 
from whooshlearn.csdn import Login, BlogScanner, BlogDetails, Searcher

login = Login()
session = login.login(username="marksinoberg", password="PRCstylewarmup")
print(session)

scanner = BlogScanner(domain="Marksinoberg")
blogs = scanner.scan()
print(blogs[0:3])

blogdetails = BlogDetails(session=session, blogurl=blogs[0])
blog = blogdetails.getSource()
print(blog['url'])
print(blog['description'])
print(blog['tags'])

# test whoosh for searcher
searcher = Searcher()
counter=1
for item in blogs[0:10]:
    print("开始处理第{}篇文章".format(counter))
    counter+=1
    details = BlogDetails(session=session, blogurl=item).getSource()
    searcher.addblog(details)
# searcher.addblog(blog)
# searcher.search('DbHelper')
# searcher.search('Python')
searcher.search("博客")