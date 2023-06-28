<<<<<<< HEAD
from bs4 import BeautifulSoup
import re
import json

# Assume 'html' contains the HTML content of the webpage
soup = BeautifulSoup(html, 'html.parser')

# Find the <script> tag containing the JavaScript object
script_tag = soup.find('script', text=re.compile(r'windows\.classified'))

# Extract the JavaScript object text
script_text = script_tag.string

# Parse the JavaScript object into a Python dictionary
data = re.search(r'(?<=windows\.classified\s=\s).*?(?=;)', script_text).group()
data_dict = json.loads(data)

# Access and process the data as needed
# For example, printing the property features and values
for key, value in data_dict.items():
    print(f"Feature: {key}, Value: {value}")
=======
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
>>>>>>> fcf6f97b1b4fd28c3629d7914d98b53a7d8979f1
