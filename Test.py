import requests, re, json
from bs4 import BeautifulSoup
from pathlib import Path
root_url = "https://www.immoweb.be"
web_url = "https://www.immoweb.be/en/classified/mixed-use-building/for-sale/gent/9000/10655537"
cookie = requests.get(root_url).cookies
resp = BeautifulSoup(requests.get(root_url, cookies=cookie).text)
print(resp.prettify())
if resp == "<Response [200]>":
    print ('OK!')
else:
    print ('Boo!')