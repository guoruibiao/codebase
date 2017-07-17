#!/usr/bin/env python
# coding: utf8
from compute import Radar

def compute(username):
    """
    计算出username对应的文章得分情况。
    """
    radar = Radar(username=username)
    catagroies = radar.get_catagories()
    for catagory in catagroies:
        # 先求出每一个分类下的所有的文章链接。然后计算出总分数
        counts = catagory['counts']
        posturls = radar.get_posts(catagory_url=catagory['url'], counts=counts)
        score = 0
        for posturl in posturls:
            try:
                score += radar.get_detail(posturl=posturl)
            except Exception as e:
                print(e)
                continue
        print('{}的总体得分为：{}'.format(catagory['name'], score))
        catagory['score'] = 0 if counts==0 else score/counts
    return catagroies