from Utils.scrape import run_scraper
# Prompt for the number of pages to scrape
num_pages = int(input("Enter the number of pages to scrape: "))

# Prompt for the number of workers
num_workers_input = input("Enter the number of workers (default is 10): ")
num_workers = int(num_workers_input) if num_workers_input else 10
# Run the scraper
run_scraper(num_pages, num_workers)