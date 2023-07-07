import asyncio
import aiohttp
import json
import pandas as pd
import os
import re
import numpy as np
from bs4 import BeautifulSoup

house_details = []
SCRAPED_URLS = set()
raw_data = []
ERROR_COUNT = 0
URL_COUNT = 0
COUNTER = 0
COUNTER_LOCK = asyncio.Lock()

selected_values = [
    ("id", "id"),
    ("Street", "property.location.street"),
    ("Housenumber", "property.location.number"),
    ("Box", "property.location.box"),
    ("Floor", "property.location.floor"),
    ("City", "property.location.locality"),
    ("Postalcode", "property.location.postalCode"),
    ("Property type", "property.location.type"),
    ("Region", "property.location.regionCode"),
    ("District", "property.location.district"),
    ("Subtype", "property.subtype"),
    ("Price", "price.mainValue"),
    ("Type of sale", "price.type"),
    ("Construction year", "property.building.constructionYear"),
    ("Bedroom Count", "property.bedroomCount"),
    ("Habitable surface", "property.netHabitableSurface"),
    ("Kitchen type", "property.kitchen.type"),
    ("Furnished", "transaction.sale.isFurnished"),
    ("Fireplace", "property.fireplaceExists"),
    ("Terrace", "property.hasTerrace"),
    ("Garden", "property.hasGarden"),
    ("Garden surface", "property.land.surface"),
    ("Facades", "property.building.facadeCount"),
    ("SwimmingPool", "property.hasSwimmingPool"),
    ("Condition", "property.building.condition"),
    ("EPC score", "transaction.certificates.epcScore"),
    ("Latitude", "property.location.latitude"),
    ("Longitude", "property.location.longitude")
    
]

async def get_property(session, url):
    """
    Fetches the property details from the given URL.

    Args:
        session (aiohttp.ClientSession): The session object to use for making the GET request.
        url (str): The URL of the property.

    Returns:
        dict: The property details as a dictionary.
    """
    try:
        async with session.get(url) as response:
            html_content = await response.text()
            start_marker = "window.classified = " #create variable for cutting the content string at the start of the dictionary
            end_marker = ";\n"                    #create variable for cutting off the end of the string
            start_index = html_content.find(start_marker) + len(start_marker) 
            end_index = html_content.find(end_marker, start_index)
            if start_index != -1 and end_index != -1: #check if we are not out of bounds with the string
                json_data = html_content[start_index:end_index] #create the dictionary from the resulting string {}
                house_dict = json.loads(json_data) #seperate dict for the filtered result
                return house_dict, json_data
    except (aiohttp.ClientError, json.JSONDecodeError) as e:
        print(f"Error occurred during scraping: {e}")
    return None, None

async def get_urls(num_pages, session):
    """
    Retrieves the list of property URLs to scrape.

    Args:
        num_pages (int): The number of pages to scrape.
        session (aiohttp.ClientSession): The session object to use for making the GET request.

    Returns:
        list: A list of property URLs.
    """
    list_all_urls = []
    global URL_COUNT # Add the global variable for URL count
    for i in range(1, num_pages + 1):
        root_url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={i}&orderBy=relevance"
        async with session.get(root_url) as response:
            content = await response.text()
        soup = BeautifulSoup(content, "html.parser")
        if response.status == 200:
            list_all_urls.extend(tag.get("href") for tag in soup.find_all("a", attrs={"class": "card__title-link"}))
            print(f'Urls found: {len(list_all_urls)}', end='\r', flush=True)
            URL_COUNT = len(list_all_urls)
        else:
            print("Page notfound.")
            break
    print(f"Number of properties: {len(list_all_urls)}")
    return list_all_urls

async def save_raw_data(version):
    """
    Saves the raw scraped data to a CSV file.

    Args:
        version (int): The version number for the CSV file.
    """
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    filename = os.path.join(root_folder, f"data/scrapes/scrape_v{version}.csv")
    raw_data_df = pd.DataFrame(raw_data)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    raw_data_df.to_csv(filename, index=False)
    print(f"Raw data saved to {filename}")

async def save_data(version):
    """
    Saves the scraped data to a CSV file.

    Args:
        version (int): The version number for the CSV file.
    """
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    filename = os.path.join(root_folder, f"data/filtered_data/house_details_v{version}.csv")
    house_details_df = pd.DataFrame(house_details)
    if not house_details_df.empty:
        house_details_df.replace({np.nan: 0, None: 0}, inplace=True)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        house_details_df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

def get_latest_version(file_prefix):
    """
    Retrieves the latest version number for the given file prefix.

    Args:
        file_prefix (str): The prefix of the CSV file.

    Returns:
        int: The latest version number.
    """
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    version = 0
    for filename in os.listdir(os.path.join(root_folder, "data/filtered_data")):
        if filename.startswith(file_prefix) and filename.endswith(".csv"):
            match = re.search(r"v(\d+)", filename)
            if match:
                file_version = int(match.group(1))
                version = max(version, file_version)
    return version


def load_data():
    """
    Loads previously scraped data from a CSV file.

    Returns:
        int: The version number of the CSV file.
    """
    latest_version = get_latest_version("house_details_v")
    version = latest_version + 1 if latest_version > 0 else 1
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    filename = os.path.join(root_folder, f"data/filtered_data/house_details_v{version}.csv")
    if latest_version > 0:
        print(f"Existing data found: version {latest_version}.\nNew version {version} will be created.")
    else:
        print(f"No existing data found.")
        print(f"Creating a new version {version} CSV file.")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            file.write('')
    return version

async def process_url(url, session):
    """
    Processes a property URL and extracts the relevant details.

    Args:
        url (str): The URL of the property.
        session (aiohttp.ClientSession): The session object to use for making the GET request.
    """
    global SCRAPED_URLS, COUNTER_LOCK, ERROR_COUNT
    if url in SCRAPED_URLS:
        return
    house_dict, raw_json_data = await get_property(session, url)
    if url in SCRAPED_URLS:
        # Skip if URL already processed
        print(f"Skipping URL: {url}")
        return
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
            filtered_house_dict[new_key] = value
        id_match = re.search(r"/(\d+)$", url)
        if id_match:
            filtered_house_dict["id"] = int(id_match.group(1))
        house_details.append(filtered_house_dict)
        raw_data.append({"json_data": raw_json_data})
    else:
        # Increment error count
        ERROR_COUNT += 1
        # Sleep for 3 seconds if property details couldn't be fetched
        await asyncio.sleep(3)

async def process_url_wrapper(url, session):
    """
    Wrapper function for processing a property URL.

    Args:
        url (str): The URL of the property.
        session (aiohttp.ClientSession): The session object to use for making the GET request.
    """
    global ERROR_COUNT
    if url in SCRAPED_URLS:
        return
    await process_url(url, session)
    async with COUNTER_LOCK:
        global COUNTER
        COUNTER += 1

async def print_progress():
    """
    Prints the progress of URL processing.
    """
    global COUNTER, URL_COUNT, ERROR_COUNT
    while COUNTER < URL_COUNT:
        print(f"URLs processed: {COUNTER}/{URL_COUNT}, Errors: {ERROR_COUNT}", end='\r', flush=True)
        await asyncio.sleep(1)
    print(f"URLs processed: {COUNTER}/{URL_COUNT}, Errors: {ERROR_COUNT}")

async def run_scraper(num_pages):
    """
    Runs the scraper to fetch property details.

    Args:
        num_pages (int): The number of pages to scrape.

    Returns:
        int: The version number of the CSV file.
    """
    version = load_data()
    async with aiohttp.ClientSession() as session:
        urls = await get_urls(num_pages, session)
        global URL_COUNT
        URL_COUNT = len(urls)  # Update URL_COUNT here
        tasks = []
        for url in urls:
            task = process_url_wrapper(url, session)
            tasks.append(task)
        progress_task = asyncio.create_task(print_progress())
        await asyncio.gather(*tasks)
        progress_task.cancel()
    #await save_raw_data(version)
    await save_data(version)
    return version