import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import os
import re
from concurrent.futures import ThreadPoolExecutor


def get_property(url, session):
    """
    Fetches the property details from the given URL.

    Args:
        url (str): The URL of the property.
        session (requests.Session): The session object to use for making the GET request.

    Returns:
        dict: The property details as a dictionary.
    """
    try:
        response = session.get(url)
        html_content = response.text
        start_marker = "window.classified = "
        end_marker = ";\n"
        start_index = html_content.find(start_marker) + len(start_marker)
        end_index = html_content.find(end_marker, start_index)
        if start_index != -1 and end_index != -1:
            json_data = html_content[start_index:end_index]
            house_dict = json.loads(json_data)
            return house_dict
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error occurred during scraping: {e}")
    return None


def get_urls(num_pages):
    """
    Retrieves the list of property URLs to scrape.

    Args:
        num_pages (int): The number of pages to scrape.

    Returns:
        list: A list of property URLs.
    """
    list_all_urls = []
    for i in range(1, num_pages + 1):
        root_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={i}&orderBy=relevance"
        req = requests.get(root_url)
        content = req.content
        soup = BeautifulSoup(content, "html.parser")
        if req.status_code == 200:
            list_all_urls.extend(tag.get("href") for tag in soup.find_all("a", attrs={"class": "card__title-link"}))
        else:
            print("Page not found")
            break
    print(f"Number of houses: {len(list_all_urls)}")
    return list_all_urls




selected_values = [
    ("id", "id"),
    ("locality", "property.location.locality"),
    ("type", "property.location.type"),
    ("subtype", "property.subtype"),
    ("mainValue", "price.mainValue"),
    ("type_of_sale", "price.type"),
    ("bedroomCount", "property.bedroomCount"),
    ("netHabitableSurface", "property.netHabitableSurface"),
    ("kitchen_type", "property.kitchen.type"),
    ("isFurnished", "transaction.sale.isFurnished"),
    ("fireplaceExists", "property.fireplaceExists"),
    ("hasTerrace", "property.hasTerrace"),
    ("hasGarden", "property.hasGarden"),
    ("surface", "property.land.surface"),
    ("facadeCount", "property.building.facadeCount"),
    ("hasSwimmingPool", "property.hasSwimmingPool"),
    ("condition", "property.building.condition")
]

house_details = []
if os.path.isfile("data/house_details.csv"):
    os.remove("data/house_details.csv")
    print("Existing data file deleted.")


def process_url(url):
    """
    Processes a property URL and extracts the relevant details.

    Args:
        url (str): The URL of the property.
    """
    session = requests.Session()
    if any(record.get("id") == url for record in house_details):
        print(f"Skipping URL: {url}")
        return
    house_dict = get_property(url, session)
    if house_dict:
        filtered_house_dict = {}
        for new_key, old_key in selected_values:
            nested_keys = old_key.split(".")
            value = house_dict
            for nested_key in nested_keys:
                if isinstance(value, dict) and nested_key in value:
                    value = value[nested_key]
                else:
                    value = None
                    break
            if isinstance(value, bool):
                value = int(value)
            if isinstance(value, float):
                value = int(value)
            filtered_house_dict[new_key] = value
        id_match = re.search(r"/(\d+)$", url)
        if id_match:
            filtered_house_dict["id"] = int(id_match.group(1))
        house_details.append(filtered_house_dict)
    else:
        time.sleep(3)
# Prompt for the number of pages to scrape
num_pages = int(input("Enter the number of pages to scrape: "))
list_of_urls = get_urls(num_pages)
max_threads = 30
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    executor.map(process_url, list_of_urls)

house_details_df = pd.DataFrame(house_details)
house_details_df.replace({np.nan: 0, None: 0}, inplace=True)
house_details_df = house_details_df.astype(int, errors='ignore')
os.makedirs("data", exist_ok=True)
house_details_df.to_csv("data/house_details.csv", index=False)
print(f"Total records: {len(house_details)}")
print(house_details_df)