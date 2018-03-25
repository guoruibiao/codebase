# coding: utf8
from hashlib import *
from constraints import servers, entries
from func import *
length = len(servers)
details1 = {key:[] for key in servers}
for entry in entries:
    # keyhash = sum([ord(c) for c in entry])
    keyhash = hashcode(entry)
    server = servers[keyhash%length]
    details1[server].append(entry)
print_pretty_dict(details1)

print("---"*28)
del servers[0]
length = len(servers)
details2 = {key:[] for key in servers}
for entry in entries:
    # keyhash = sum([ord(c) for c in entry])
    keyhash = hashcode(entry)
    server = servers[keyhash%length]
    details2[server].append(entry)
print_pretty_dict(details2)

print("---"*28)
servers.insert(0, "192.168.0.1:11211")
servers.append("192.168.0.5:11211")
length = len(servers)
details3 = {key:[] for key in servers}
for entry in entries:
    # keyhash = sum([ord(c) for c in entry])
    keyhash = hashcode(entry)
    server = servers[keyhash%length]
    details3[server].append(entry)
print_pretty_dict(details3)

# -------计算缓存度
print("==="*7)
print_pretty_dict(compute_cache_percentage(details1, details2))
print("---"*20)
print_pretty_dict(compute_cache_percentage(details1, details3))