from scraper.base_scraper import BaseScraper
from utils.job_parser import parse_job_listing
from urllib.parse import urljoin
import time

class SqlinkScraper(BaseScraper):
    def scrape(self):
        next_page_url = self.base_url

        while next_page_url:
            self.failed_logger.info(f'Scraping page: {next_page_url}')
            
            try:
                soup = self.fetch_page(next_page_url)
                job_container = soup.find('div', id='searchResultsList')

                if job_container:
                    job_listings = job_container.find_all('div', class_='positionItem')
                else:
                    job_listings = soup.find_all('div', class_='positionItem')
                
                if not job_listings:
                    self.failed_logger.warning(f'No job listings found on {next_page_url}')
                    break

                jobs = []

                for job in job_listings:
                    job_data = parse_job_listing(job, self.platform_name)
                    if job_data:
                        jobs.append(job_data)

                self.save_jobs(jobs)

                next_button = soup.find('li', id='rightLeft')
                if not next_button or not next_button.find('a', href=True):
                    self.failed_logger.info(f'No more pages to scrape. Finished on current page.')
                    break

                relative_next_page = next_button.find('a', href=True)['href']
                next_page_url = urljoin(self.base_url, relative_next_page)
                time.sleep(self.sleep_interval)

            except Exception as e:
                self.failed_logger.error(f'Error scraping {next_page_url}: {e}')
                break

        self.close()
