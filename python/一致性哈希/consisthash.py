# coding: utf8
# 简单一致性hash实现

from constraints import servers, entries
from func import print_pretty_dict, hashcode, compute_cache_percentage, compute_cache_percentage_ring


class ConsistHash(object):
	"""
	简单一致性哈希算法实现
	"""
	def __init__(self, servers=[]):
		self.servers = servers
		# sorted list which contains server nodes.
		self.ring = []
		# node:[hashcode1, hashcode2, ...]
		self.hashnodemap = {}
		for server in self.servers:
			self.addNode(server)

	def addNode(self, node):
		code = hashcode(node)
		self.hashnodemap[code] = node
		self.ring.append(code)
		self.ring.sort()


	def removeNode(self, node):
		del self.hashnodemap[hashcode(node)]
		self.ring.remove(hashcode(node))

	def getNode(self, key):
		code = hashcode(key)
		for ringitem in self.ring[::-1]:
			if ringitem <= code:
				return self.hashnodemap[ringitem]
		return self.hashnodemap[self.ring[0]]


class Cacher(object):
	"""
    普通一致性哈希算法的应用
	"""
	def __init__(self, servers):
		self.c = ConsistHash(servers=servers)
		self.container = {key:[] for key in servers}

	def addServer(self, server):
		self.c.addNode(server)
		self.container[server] = []

	def removeServer(self, server):
		self.c.removeNode(server)
		del self.container[server]

	def cache(self, key, value):
		server = self.c.getNode(key)
		self.container[server].append({key: value})


	def get(self, key):
		server = self.c.getNode(key)
		return self.container[server].items()[key]


if __name__ == "__main__":
	# c = ConsistHash(servers=servers)
	# print_pretty_list(c.ring)
	# print_pretty_dict(c.hashnodemap)
	cacher1 = Cacher(servers)
	for entry in entries:
		cacher1.cache(entry, entry)
	print_pretty_dict(cacher1.container)
	# 删除一个服务器
	cacher3 = Cacher(servers)
	cacher3.removeServer("192.168.0.1:11211")
	for entry in entries:
		cacher3.cache(entry, entry)
	print_pretty_dict(cacher3.container)
	# 添加一个服务器
	cacher2 = Cacher(servers)
	cacher2.addServer("192.168.0.5:11211")
	for entry in entries:
		cacher2.cache(entry, entry)
	print_pretty_dict(cacher2.container)
	# 计算缓存有效度
	print_pretty_dict(compute_cache_percentage_ring(cacher1.container, cacher2.container))
	print_pretty_dict(compute_cache_percentage_ring(cacher1.container, cacher3.container))



