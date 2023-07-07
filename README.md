
# Web Scraping project - Dataset of properties in Belgium

## Description of the project:
This is a web scraping project which is made for collecting information about a wide range of properties located all over Belgium.
* The goal is to build a comprehensive dataset that includes details about 10,000 properties such as propertytype, location, price, size and other attributes.
* The purpose of this project is to collect data from a website that provide property listing in Belgium. 
* By using web scraping techniques, we can extract the information from the source(www.immoweb.be) and compile into a structured dataset for further prediction, analysis, research or any other purpose.

## Installation
To use this web-scraping project, you need to meet the following requirements:
* Minimum Python 3.9 version installed on your system.
* Install required libraries listed in the requirements.txt file in the repo main branch.
  ### how to install requirements:
  
    Open up a terminal or a command prompt and navigate to the directory of your Python project.
    Once you are there, type the following command:

    pip install -r requirements.txt
  
  
## Usage
* Clone the project repository from GitHub [link]( https://github.com/Sam-Veldeman/challenge-collecting-data).
* Open a terminal or command prompt and navigate to the project directory "challenge-collecting-data", there you should see main.py file .
* Now, Run the following command to start the scraping (python3 scraper.py) and input the number of pages(60 listings per page) you 
  want to scrape and the number of workers u like to use for concurency. (no input will use std 10 workers)
* Execute the main.py script to initiate the web scraping process. The filtered scraped data will be collected and stored in
  data/filtered_data/house_details_(version number).csv file. The raw data will be stored in the /data/scrapes/scrape_(version number).csv file. The version numbers depends on what version numbers are allready present in the folders.

## Update 06/07/2023
* Added an async scraper, it is a bit faster than the original one.
* Usage is the same as the original scraper, only this time use the async_main.py to start the scrape.
* This scraper has no option to choose the amount of workers, since it is working asyncro.

### Contributors
This project is done by Sam Veldeman,Wouter Daneels and Monisha Hitang learners of AI Bootcamp at Becode.org and assisted by the coaches Vanessa Rivera Quinones and Samuel Borms. 

### Timeline
This project is completed in about 5 days. This project is done during 26 june - 30 june, 2023.

### Personal situation
This project is done as a part of group project of AI Bootcamp course. As learners of “AI Bootcamp” course at Becode.org, we were given this project to do as a part of our coursework. This project was very helpful for us to use the concepts we have learned such as Python programming  language, web-scraping, file-handeling, regex, concurrency etc. 