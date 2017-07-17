# coding: utf8

import requests

username = "zhangsan"
password = "zhadsadsadngsan"

url = "http://localhost/learn/accesscontrol/http.php"

response = requests.get(url=url, auth=(username, password))
# response = requests.get(url=url)
print(response.status_code)

print(response.text)


