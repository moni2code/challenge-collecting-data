import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import threading
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
        response = session.get(url)  # Send GET request to the URL
        html_content = response.text  # Get the HTML content of the response
        start_marker = "window.classified = "
        end_marker = ";\n"
        start_index = html_content.find(start_marker) + len(start_marker)  # Find the start index of the property details JSON
        end_index = html_content.find(end_marker, start_index)  # Find the end index of the property details JSON
        if start_index != -1 and end_index != -1:
            json_data = html_content[start_index:end_index]  # Extract the property details JSON
            house_dict = json.loads(json_data)  # Parse the JSON into a dictionary
            house_dict['url'] = url  # Add the 'url' key to the house_dict
            return house_dict
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error occurred during scraping: {e}")
    return None


def get_urls(num_pages, session):
    """
    Retrieves the list of property URLs to scrape.

    Args:
        num_pages (int): The number of pages to scrape.
        session (requests.Session): The session object to use for making the GET requests.

    Returns:
        list: A list of property URLs.
    """
    list_all_urls = []
    for page in range(1, num_pages + 1):
        root_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page}&orderBy=relevance"
        req = session.get(root_url)  # Send GET request to the root URL
        content = req.content  # Get the content of the response
        soup = BeautifulSoup(content, "html.parser")  # Create a BeautifulSoup object for parsing HTML
        if req.status_code == 200:
            # Find all <a> tags with class "card__title-link" and extract the 'href' attribute
            list_all_urls.extend(tag.get("href") for tag in soup.find_all("a", attrs={"class": "card__title-link"}))
        else:
            print("Page not found")
        # Introduce a sleep interval between requests to avoid overwhelming the server
        time.sleep(1)

    print(f"Number of houses: {len(list_all_urls)}")
    return list_all_urls


# Set the number of pages to scrape
num_pages = 1

# Create the session object
session = requests.Session()

# Set the maximum number of threads
max_threads = 50

# Create a ThreadPoolExecutor to process URLs in parallel
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Get the list of property URLs in a multithreaded manner
    list_of_urls = executor.submit(get_urls, num_pages, session).result()

    # Process each URL in parallel using executor.map()
    house_details = executor.map(lambda url: get_property(url, session), list_of_urls)

# Filter out any None values from house_details list
house_details = [house for house in house_details if house is not None]

# Define the selected values to extract from the property details
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

house_details_processed = []  # List to store processed property details
duplicate_listings = []  # List to store duplicate listings

# Delete the csv file if it already exists to always start with an empty file
if os.path.isfile("data/house_details.csv"):
    os.remove("data/house_details.csv")
    print("Existing data file deleted.")

def process_property(house_dict):
    """
    Processes a property dictionary and extracts the relevant details.

    Args:
        house_dict (dict): The dictionary containing the property details.
    """
    filtered_house_dict = {}  # Dictionary to store filtered property details
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
    id_match = re.search(r"/(\d+)$", house_dict['url'])
    if id_match:
        filtered_house_dict["id"] = int(id_match.group(1))

    # Check for duplicate listings
    address = house_dict.get("property", {}).get("location", {}).get("address")
    if address:
        is_duplicate = any(record.get("address") == address for record in house_details_processed)
        if is_duplicate:
            filtered_house_dict["address"] = address
            duplicate_listings.append(filtered_house_dict)
            print(f"Flagged duplicate listing: {house_dict['url']}")
        else:
            house_details_processed.append(filtered_house_dict)
    else:
        house_details_processed.append(filtered_house_dict)


# Process each property in parallel using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    executor.map(process_property, house_details)

# Create dataframes for the processed property details
house_details_df = pd.DataFrame(house_details_processed)
house_details_df.replace({np.nan: 0, None: 0}, inplace=True)
house_details_df = house_details_df.astype(int, errors='ignore')

duplicate_listings_df = pd.DataFrame(duplicate_listings)
duplicate_listings_df.replace({np.nan: 0, None: 0}, inplace=True)
duplicate_listings_df = duplicate_listings_df.astype(int, errors='ignore')

# Save the dataframes to CSV files
house_details_df.to_csv("data/house_details.csv", index=False)
duplicate_listings_df.to_csv("data/duplicate_listings.csv", index=False)

print(f"Total records: {len(house_details_processed)}")
print(house_details_df)
print(f"Total duplicate listings: {len(duplicate_listings)}")
print(duplicate_listings_df)
