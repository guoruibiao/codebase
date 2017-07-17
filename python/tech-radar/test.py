from compute import Radar

radar = Radar(username='qq_29883591')


catagroies = radar.get_catagories()
for catagory in catagroies:
    # 先求出每一个分类下的所有的文章链接。然后计算出总分数
    posturls = radar.get_posts(catagory_url=catagory['url'], counts=catagory['counts'])
    score = 0
    for posturl in posturls:
        score += radar.get_detail(posturl=posturl)
    print('{}的总体得分为：{}'.format(catagory['name'], score))
    catagory['score'] = score




