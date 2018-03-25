# coding: utf8
# 带有虚拟节点的一致性哈希算法实现

from constraints import servers, entries
from func import print_pretty_dict, hashcode, print_pretty_list
from func import compute_cache_percentage
from func import compute_cache_percentage_ring
from func import compute_cache_percentage_virtual_ring

class VirtualConsistHash(object):
    """
    带有虚拟节点的一致性哈希算法实现
    """
    def __init__(self, servers=[], replicas=3):
        self.servers = servers
        # sorted list which contains server nodes.
        self.ring = []
        # node:[hashcode1, hashcode2, ...]
        # 虚拟节点的个数，其实这个名字叫虚拟节点的个数不太合适，每个真实节点“虚拟化”后的节点个数比较好
        self.replicas = replicas
        self.hashnodemap = dict()
        for server in self.servers:
            self.addNode(server)

    def addNode(self, node):
        for i in range(0, self.replicas):
            temp = "{}#{}".format(node, i)
            code = hashcode(temp)
            self.hashnodemap[code] = temp
            self.ring.append(code)
            self.ring.sort()

    def removeNode(self, node):
        for i in range(0, self.replicas):
            temp = "{}#{}".format(node, i)
            code = hashcode(temp)
            self.ring.remove(code)
            del self.hashnodemap[code]
           
    def getNode(self, key):
        code = hashcode(key)
        for ringitem in self.ring[::-1]:
            if ringitem <= code:
                return self.hashnodemap[ringitem]
        return self.hashnodemap[self.ring[0]]


class Cacher(object):
    """
    带有虚拟节点的一致性哈希算法的应用
    """
    def __init__(self, servers):
        self.c = VirtualConsistHash(servers=servers)
        self.container = {"{}#{}".format(server, index): [] for index in range(0, self.c.replicas) for server in self.c.servers}

    def addServer(self, server):
        self.c.addNode(server)
        for i in range(0, self.c.replicas):
            temp = "{}#{}".format(server, i)
            self.container[temp] = []

    def removeServer(self, server):
        self.c.removeNode(server)
        for i in range(0, self.c.replicas):
            temp = "{}#{}".format(server, i)
            del self.container[temp]

    def cache(self, key, value):
        server = self.c.getNode(key)
        self.container[server].append({key: value})

    def get(self, key):
        server = self.c.getNode(key)
        return self.container[server].items()[key]


if __name__ == "__main__":
    c = VirtualConsistHash(servers=servers)
    print_pretty_list(c.ring)
    print_pretty_dict(c.hashnodemap)
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
    print("==="*19, "删除一个缓存服务器后~")
    print_pretty_dict(
        compute_cache_percentage_virtual_ring(cacher1.container, cacher2.container))
    print("==="*19, "添加一个缓存服务器后~")
    print_pretty_dict(
        compute_cache_percentage_virtual_ring(cacher1.container, cacher3.container))