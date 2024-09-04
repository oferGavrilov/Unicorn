from scraper.scraper_manager import ScraperManager
from utils.logger import configure_failed_logger
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def main():
    platform_name = 'sqlink'
    platform_url = 'https://www.sqlink.com/career/%D7%A4%D7%99%D7%AA%D7%95%D7%97-%D7%AA%D7%95%D7%9B%D7%A0%D7%94-webmobile/'

    failed_logger = configure_failed_logger(platform_name)

    scraper_manager = ScraperManager(MONGO_URI, DB_NAME, COLLECTION_NAME)
    scraper_manager.scrape(platform_name, platform_url, failed_logger)

if __name__ == '__main__':
    main()
