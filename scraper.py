import time
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from utils.job_parser import parse_job_listing
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, SLEEP_INTERVAL

logger = logging.getLogger(__name__)

def scrape(platform_name, platform_url):
    # Initialize MongoDB collection
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    job_collection = db[COLLECTION_NAME]

    next_page_url = platform_url

    while next_page_url:
        logger.info(f'Scraping page: {next_page_url}')
        
        try:
            response = requests.get(next_page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            job_container = soup.find('div', id='searchResultsList')

            if job_container:
                job_listings = job_container.find_all('div', class_='positionItem')
            else:
                job_listings = soup.find_all('div', class_='positionItem')
            
            if not job_listings:
                logger.warning(f'No job listings found on {next_page_url}')
                break

            jobs = []

            for job in job_listings:
                job_data = parse_job_listing(job, platform_name)
                if job_data:
                    jobs.append(job_data)

            if jobs:
                job_collection.insert_many(jobs)
                logger.info(f'Successfully scraped and stored {len(jobs)} jobs from {next_page_url}')
            else:
                logger.warning(f'No jobs found on {next_page_url}')
                break

            next_button = soup.find('li', id='rightLeft')
            if not next_button or not next_button.find('a', href=True):
                logger.info(f'No more pages to scrape. Finished on current page.')
                break

            relative_next_page = next_button.find('a', href=True)['href']
            next_page_url = urljoin(platform_url, relative_next_page)
            time.sleep(SLEEP_INTERVAL)

        except Exception as e:
            logger.error(f'Error scraping {next_page_url}: {e}')
            break

    # Close MongoDB connection
    client.close()
