from utils.logger import setup_logging
from scraper import scrape
from config import BASE_URL, PLATFORM_NAME

if __name__ == '__main__':
    logger = setup_logging()
    scrape(PLATFORM_NAME, BASE_URL)
