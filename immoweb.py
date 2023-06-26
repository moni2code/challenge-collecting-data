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