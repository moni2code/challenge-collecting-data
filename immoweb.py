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