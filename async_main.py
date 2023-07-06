from Utils.async_scrape import run_scraper
import asyncio

async def main():
    # Prompt for the number of pages to scrape
    num_pages = int(input("Enter the number of pages to scrape: "))
    await run_scraper(num_pages)

if __name__ == '__main__':
    asyncio.run(main())