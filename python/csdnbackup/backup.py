# coding: utf8

# @Author: 郭 璞
# @File: backup.py                                                                 
# @Time: 2017/4/28                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: Back up the blog for getting and stroaging the markdown file.
import json
import os
import re
import random
import time

class Backup(object):
    """
    Get the special url for getting markdown file.
    """
    def __init__(self, session, backupurl):
        self.headers = {
            'Referer': 'http://write.blog.csdn.net/mdeditor',
            'Host': 'passport.csdn.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }
        # constructor the url: get article id and the username
        # http://blog.csdn.net/marksinoberg/article/details/70432419
        username, id = backupurl.split('/')[3], backupurl.split('/')[-1]
        self.backupurl = 'http://write.blog.csdn.net/mdeditor/getArticle?id={}&username={}'.format(id, username)
        self.session = session
    def getSource(self):
        # get title and content for the assigned url.
        try:
            tempheaders = self.headers
            tempheaders['Referer'] = 'http://write.blog.csdn.net/mdeditor'
            tempheaders['Host'] = 'write.blog.csdn.net'
            tempheaders['X-Requested-With'] = 'XMLHttpRequest'
            response = self.session.get(url=self.backupurl, headers=tempheaders)
            soup = json.loads(response.text)
            return {
                'title': soup['data']['title'],
                'markdowncontent': soup['data']['markdowncontent'],
            }
        except Exception as e:
            print("接口请求失败! 详细信息为：{}".format(e))


    def downloadpic(self, picurl, outputpath):
        time.sleep(random.randint(1,3))
        try:
            tempheaders = self.headers
            tempheaders['Host'] = 'img.blog.csdn.net'
            tempheaders['Upgrade-Insecure-Requests'] = '1'
            response = self.session.get(url=picurl, headers=tempheaders)
            print(response.status_code)
            # change the seperator of your OS
            outputpath = outputpath.replace(os.sep, '/')
            print(outputpath)
            if response.status_code == 200:
                with open(outputpath, 'wb') as f:
                    f.write(response.content)
                    f.close()
                    print("{} saved in {} succeed!".format(picurl, outputpath))
            else:
                raise Exception("Picture Url: {} downloading failed!".format(picurl))
        except Exception as e:
            print('图片{}下载失败！{}'.format(picurl, e))

    def getpicurls(self):
        pattern = re.compile("\!\[.*?\]\((.*)?\)")
        markdowncontent = self.getSource()['markdowncontent']
        return re.findall(pattern=pattern, string=markdowncontent)

    def backup(self, outputpath='./'):
        try:
            source = self.getSource()
            foldername = source['title']
            foldername = os.path.join(outputpath, foldername)
            if not os.path.exists(foldername):
                os.mkdir(foldername)
            # write file
            filename = os.path.join(foldername, source['title'])

            with open(filename+".md", 'w', encoding='utf8') as f:
                f.write(source['markdowncontent'])
                f.close()
                print("{}.md 下载完毕，保存路径为：{}".format(filename, outputpath))
            # save pictures
            imgfolder = os.path.join(foldername, 'img')
            if not os.path.exists(imgfolder):
                os.mkdir(imgfolder)
            for index, picurl in enumerate(self.getpicurls()):
                imgpath = imgfolder + os.sep+str(index)+'.png'
                try:
                    self.downloadpic(picurl=picurl, outputpath=imgpath)
                except:
                    # 有可能出现： requests.exceptions.TooManyRedirects: Exceeded 30 redirects.
                    pass
        except Exception as e:
            print('恩，又出错了。详细信息为：{}'.format(e))
            pass




