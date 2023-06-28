<<<<<<< HEAD
import requests
import re
from bs4 import BeautifulSoup
import json

def get_property():
    # Make a GET request to fetch the HTML content of the page
    url = "https://www.immoweb.be/en/classified/mixed-use-building/for-sale/gent/9000/10655537"  # Replace with the URL of the page containing the data
    response = requests.get(url)
    html_content = response.text
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")
    # Find the script tag containing the desired data
    script_tag = soup.find("script", string=lambda text: text and "window.classified" in text)
    if script_tag:
        # Extract the data within the script tag
        script_content = script_tag.string.strip()
        # Remove the "window.classified =" prefix and removing all the whitespace and clutter in the suffix to get only the dictionary to parse into the JSON_data.
        pattern = r"window\.classified = ({.*?});"
        match = re.search(pattern, script_content)
    if match:
        json_data = match.group(1)
        # Load the JSON data into a dictionary
        house_dict = json.loads(json_data)
        # Clean the data in the dictionary by key values
        keys_to_delete = ["cluster", "customers", "features", "premiumProjectPage", "media", "alternativeDescriptions", "hasSectionsArray", "displayFlags"]
        house_dict = {key: value for key, value in house_dict.items() if key not in keys_to_delete}
    return house_dict
# Function to itterate over all nested dictionaries in house_dict
def extract_nested_values(data, keys_to_extract, prefix=""):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if key in keys_to_extract:
                results.append((new_prefix, value))
            results.extend(extract_nested_values(value, keys_to_extract, prefix=new_prefix))
    return results
house_dict = get_property()
# Multiple "type" keys in the dictionary
kitchen_type = house_dict['property']['kitchen']['type']
#list of key values for the excercise asignment
list_key_values =[
    "locality", "type", "subtype", "mainValue", "type_of_sale", "bedroomCount",
    "netHabitableSurface", kitchen_type, "isFurnished","fireplaceExists", "hasTerrace",
    "hasgarden", "surface", "facadeCount", "hasSwimmingPool","condition"]
key_values = extract_nested_values(house_dict, list_key_values)
print(key_values)
=======
import requests, re, json
from bs4 import BeautifulSoup
from pathlib import Path
session = requests.Session()
web_url = "https://www.immoweb.be/en/classified/mixed-use-building/for-sale/gent/9000/10655537"
#cookie = session.get(web_url).cookies
soup = BeautifulSoup(session.get(web_url,cookies=cookie).text, "html.parser")
for values in 
values_interior = session.get
def get_house_data():
    #session = requests.Session()
    cookie = session.get(web_url).cookies              # makes a cookies request using the session method from requests. 
    house = session.get(web_url, cookies=cookie)  # makes house request using the session method from requests.  
    house_data = {house: requests.get(web_url, params={"country": country}, cookies=cookie).json() for country in requests.get(urls['countries_url'], cookies=cookie).json()}
    for country in countries.json():
        while True:
            try:
                leaders = requests.get(urls['leaders_url'], params= {"country": country}, cookies=cookie)
                if leaders.status_code == 403:  # Check if cookies have expired
                    cookie = session.get(urls['cookie_url']).cookies  # Refresh the cookies
                    continue
                else:
                    leaders = leaders.json()
                    leaders_per_country[country] = []
                    for leader in leaders:
                        leader["first_paragraph"] = get_first_paragraph(leader["wikipedia_url"], session)
                        leaders_per_country[country].append(leader)
                        print(f"Name: {leader['first_name']} {leader['last_name']}")
                        print(f"First Paragraph: {leader['first_paragraph']}")
                        print()
                break
            except Exception as e:
                print(f"An error occurred for country '{country}': {str(e)}")
                break
    return leaders_per_country
print(soup)
>>>>>>> fcf6f97b1b4fd28c3629d7914d98b53a7d8979f1
