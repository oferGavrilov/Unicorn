from datetime import datetime
from utils.logger import configure_failed_logger
from utils.classifier import classify_job_position
from utils.skill_extractor import extract_requirements

def log_unclassified_or_empty_requirements(failed_logger, job_url, title, reason):
    failed_logger.warning(f"{title} URL: {job_url} - Reason: {reason}")

def parse_job_listing(job, platform_name):
    failed_logger = configure_failed_logger(platform_name)

    try:
        title = job.find('h3').text.strip()
        job_url = job.find('a', href=True)['href']
        description = job.find('section', class_='description').find('p').text.strip()

        requirements_section = job.find('section', class_='requirements')
        if requirements_section:
            for br in requirements_section.find_all('br'):
                br.replace_with('\n')
            requirements_text = requirements_section.get_text(separator="\n").strip()
        else:
            requirements_text = ""

        job_id = job.find('section', class_='description number').text.split(':')[-1].strip()
        job_position = classify_job_position(title, description)
        job_requirements = extract_requirements(requirements_text)

        if job_position == 'Other':
            log_unclassified_or_empty_requirements(failed_logger, job_url, "Position", "Missing job position")

        if not job_requirements:
            log_unclassified_or_empty_requirements(failed_logger, job_url, "Requirements", "Empty requirements")

        return {
            'job_id': job_id,
            'job_position': job_position,
            'platform': platform_name,
            'title': title,
            'description': description,
            'requirements': job_requirements,
            'url': job_url,
            'date_posted': datetime.now(),
            'scraped_at': datetime.now(),
        }
    except Exception as e:
        failed_logger.error(f'Error processing job listing: {e}')
        return None
