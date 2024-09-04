import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from utils.logger import get_logger
from config import SLEEP_INTERVAL

logger = get_logger(__name__)

class BaseScraper:
    def __init__(self, platform_name, base_url, db_uri, db_name, collection_name, failed_logger):
        self.platform_name = platform_name
        self.base_url = base_url
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.failed_logger = failed_logger
        self.sleep_interval = SLEEP_INTERVAL

    def fetch_page(self, url):
        logger.info(f'Scraping page: {url}')
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def save_jobs(self, jobs):
        if jobs:
            self.collection.insert_many(jobs)
            logger.info(f'Successfully scraped and stored {len(jobs)} jobs.')
        else:
            logger.warning(f'No jobs found.')

    def close(self):
        self.client.close()

    def scrape(self):
        raise NotImplementedError("Scrape method must be implemented by subclass.")
