#coding: utf8

from hashlib import md5

def hashcode(key=""):
    if key == None or key == "":
    	return 0
    return int(md5(str(key).encode('utf8')).hexdigest(), 16)


def print_pretty_list(ls=[]):
	for item in ls:
		print(item)

def print_pretty_dict(dc={}):
	for key, value in dc.items():
		print(f'{key}: {value}')

def compute_cache_percentage(oldcache, newcache):
	result = {key: 0 for key in oldcache.keys()}
	for key, value in oldcache.items():
		if key in newcache.keys():
			result[key] = len(list(set(value).intersection(set(newcache[key]))))
	return result

def get_map_list_key(maplist):
	result = []
	for map in maplist:
		result.extend(map.keys())
	return result

def compute_cache_percentage_ring(oldcache, newcache):
	result = {key: 0 for key in oldcache.keys()}
	# 这里每一个value其实都是一个装了字典map的列表
	for node, maplist in oldcache.items():
		if node in newcache.keys():
			oldkeys = get_map_list_key(maplist)
			newkeys = get_map_list_key(newcache[node])
			result[node] = len(list(set(oldkeys).intersection(set(newkeys))))
	return result

def compute_cache_percentage_virtual_ring(oldcache, newcache):
    result = {key.split("#")[0]: 0 for key in oldcache.keys()}
    # 这里每一个value其实都是一个装了字典map的列表
    for node, maplist in oldcache.items():
        if node in newcache.keys():
            oldkeys = get_map_list_key(maplist)
            newkeys = get_map_list_key(newcache[node])
            temp = str(node).split("#")[0]
            result[temp] += len(list(set(oldkeys).intersection(set(newkeys))))
    return result
