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