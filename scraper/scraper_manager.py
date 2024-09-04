from scraper.sqlink_scraper import SqlinkScraper

class ScraperManager:
    def __init__(self, db_uri, db_name, collection_name):
        self.db_uri = db_uri
        self.db_name = db_name
        self.collection_name = collection_name

    def scrape(self, platform_name, platform_url, failed_logger):
        if platform_name == 'sqlink':
            scraper = SqlinkScraper(
                platform_name, 
                platform_url, 
                self.db_uri, 
                self.db_name, 
                self.collection_name,
                failed_logger
            )
            scraper.scrape()
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")
