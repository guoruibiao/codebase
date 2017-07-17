# coding: utf8

# @Author: 郭 璞
# @File: csdn.py                                                                 
# @Time: 2017/5/12                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 对于CSDN本人博客的伪站内搜索实现。
import requests
from bs4 import BeautifulSoup
import json
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer, Tokenizer, Token
from whoosh.qparser import QueryParser
import jieba
import os

class Login(object):
    """
    Get the same session for blog's backing up. Need the special username and password of your account.
    """

    def __init__(self):
        # the common headers for this login operation.
        self.headers = {
            'Host': 'passport.csdn.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }

    def login(self, username, password):
        if username and password:
            self.username = username
            self.password = password
        else:
            raise Exception('Need Your username and password!')

        loginurl = 'https://passport.csdn.net/account/login'
        # get the 'token' for webflow
        self.session = requests.Session()
        response = self.session.get(url=loginurl, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Assemble the data for posting operation used in logining.
        self.token = soup.find('input', {'name': 'lt'})['value']

        payload = {
            'username': self.username,
            'password': self.password,
            'lt': self.token,
            'execution': soup.find('input', {'name': 'execution'})['value'],
            '_eventId': 'submit'
        }
        response = self.session.post(url=loginurl, data=payload, headers=self.headers)
        print("测试链接是否成功！{}".format(response.text))

        # get the session
        return self.session if response.status_code == 200 else None


class BlogScanner(object):
    """
    Scan for all blogs
    """

    def __init__(self, domain):
        self.username = domain
        self.rooturl = 'http://blog.csdn.net'
        self.bloglinks = []
        self.headers = {
            'Host': 'blog.csdn.net',
            'Upgrade - Insecure - Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }

    def scan(self):
        # get the page count
        response = requests.get(url=self.rooturl + "/" + self.username, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        pagecontainer = soup.find('div', {'class': 'pagelist'})
        pages = re.findall(re.compile('(\d+)'), pagecontainer.find('span').get_text())[-1]

        # construnct the blog list. Likes: http://blog.csdn.net/Marksinoberg/article/list/2
        for index in range(1, int(pages) + 1):
            # get the blog link of each list page
            listurl = 'http://blog.csdn.net/{}/article/list/{}'.format(self.username, str(index))
            response = requests.get(url=listurl, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                alinks = soup.find_all('span', {'class': 'link_title'})
                # print(alinks)
                for alink in alinks:
                    link = alink.find('a').attrs['href']
                    link = self.rooturl + link
                    self.bloglinks.append(link)
            except Exception as e:
                print('出现了点意外！\n' + e)
                continue

        return self.bloglinks


class BlogDetails(object):
    """
    Get the special url for getting markdown file.
    'url':博客URL
    'title': 博客标题
    'tags': 博客附属标签
    'description': 博客摘要描述信息
    'content': 博客Markdown源码
    """

    def __init__(self, session, blogurl):
        self.headers = {
            'Referer': 'http://write.blog.csdn.net/mdeditor',
            'Host': 'passport.csdn.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }
        # constructor the url: get article id and the username
        # http://blog.csdn.net/marksinoberg/article/details/70432419
        username, id = blogurl.split('/')[3], blogurl.split('/')[-1]
        self.blogurl = 'http://write.blog.csdn.net/mdeditor/getArticle?id={}&username={}'.format(id, username)
        self.session = session

    def getSource(self):
        # get title and content for the assigned url.
        try:
            tempheaders = self.headers
            tempheaders['Referer'] = 'http://write.blog.csdn.net/mdeditor'
            tempheaders['Host'] = 'write.blog.csdn.net'
            tempheaders['X-Requested-With'] = 'XMLHttpRequest'
            response = self.session.get(url=self.blogurl, headers=tempheaders)
            soup = json.loads(response.text)
            return {
                'url': soup['data']['url'],
                'title': soup['data']['title'],
                'tags': soup['data']['tags'],
                'description': soup['data']['description'],
                'content': soup['data']['markdowncontent'],
            }
        except Exception as e:
            print("接口请求失败! 详细信息为：{}".format(e))


class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False, keeporiginal=False,
                 removestops=True, start_pos=0, start_char=0, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode"%value
        t = Token(positions=positions, chars=chars, removestops=removestops, mode=mode, **kwargs)
        # 使用jieba分词，分解中文
        seglist = jieba.cut(value, cut_all=False)
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos = start_pos + value.find(w)
            if chars:
                t.startchar = start_char + value.find(w)
                t.endchar = start_pos + value.find(w) + len(w)
            yield t

def ChineseAnalyzer():
    return ChineseTokenizer()


class Searcher(object):
    """
    Firstly： define a schema suitable for this system. It may should be hard-coded.
            'url':博客URL
            'title': 博客标题
            'tags': 博客附属标签
            'description': 博客摘要描述信息
            'content': 博客Markdown源码
    Secondly: add documents(blogs)
    Thridly: search user's query string and return suitable high score blog's paths.
    """
    def __init__(self):
        # define a suitable schema
        self.schema = Schema(url=ID(stored=True),
                             title=TEXT(stored=True),
                             tags=KEYWORD(commas=True),
                             description=TEXT(stored=True),
                             content=TEXT(analyzer=ChineseAnalyzer()))
        # initial a directory to storage indexes info
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        self.indexdir = "indexdir"
        self.indexer = create_in(self.indexdir, schema=self.schema)


    def addblog(self, blog):
        writer = self.indexer.writer()
        # write the blog details into indexes
        writer.add_document(url=blog['url'],
                            title=blog['title'],
                            tags=blog['tags'],
                            description=blog['description'],
                            content=blog['content'])
        writer.commit()

    def search(self, querystring):
        # make sure the query string is unicode string.
        # querystring = u'{}'.format(querystring)
        with self.indexer.searcher() as seracher:
            query = QueryParser('content', self.schema).parse(querystring)
            results = seracher.search(query)
            # for item in results:
            #     print(item)
            hitresults = []
            for item in results:
                hitresults.append(item)
            return hitresults