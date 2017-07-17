# coding: utf8

# @Author: 郭 璞
# @File: quickstart.py                                                                 
# @Time: 2017/5/11                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 入门级QuickStart示例
from whoosh.index import create_in
from whoosh.fields import *
# 要在搜索结果中展示出来，stored属性就需要设置为True
schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
                content=TEXT(stored=True))
ix = create_in("indexdir", schema=schema)
writer = ix.writer()
writer.add_document(title=u'First Document', path=r'data/first.doc', content=u"This is the first document we've added! fuck off")
writer.add_document(title=u'Second Document', path=r'data/second.doc', content=u"This is the Second document we've added, fuck damnt!")
writer.commit()
# begin to search
from whoosh.qparser import QueryParser
# define costom querier statement
from whoosh.query import And, Term, Or

# myquery = And([Term(u"first"), Term(u"second")])

from whoosh import scoring
with ix.searcher(weighting=scoring.TF_IDF) as seracher:
    query = QueryParser("content", ix.schema).parse(u'fuck')
    results = seracher.search(query)
    for item in results:
        print(item.highlights('content'))



