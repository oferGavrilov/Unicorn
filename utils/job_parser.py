import os
import re
from datetime import datetime
import logging

def configure_failed_logger(platform_name):
    os.makedirs('logs', exist_ok=True)

    current_date = datetime.now().strftime('%d%m%y')
    log_file_name = f'logs/failed-{platform_name}-{current_date}.log'

    failed_logger = logging.getLogger('failed_jobs')
    failed_logger.setLevel(logging.WARNING)

    if failed_logger.hasHandlers():
        failed_logger.handlers.clear()

    failed_handler = logging.FileHandler(log_file_name, mode='a', encoding='utf-8')
    failed_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M'))
    failed_logger.addHandler(failed_handler)

    return failed_logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def classify_job_position(title, description):
    title = title.lower()
    description = description.lower()

    if 'full stack' in title or 'full stack' in description:
        return 'Fullstack'
    elif 'backend' in title or 'backend' in description:
        return 'Backend'
    elif 'frontend' in title or 'frontend' in description:
        return 'Frontend'
    elif 'מפתח/ת תוכנה' in title or 'מפתח/ת תוכנה' in description:
        return 'Software Developer'
    elif 'מהנדס/ת תוכנה' in title or 'מהנדס/ת תוכנה' in description:
        return 'Software Engineer'
    elif 'software engineer' in title or 'software developer' in title:
        return 'Software Engineer'
    elif 'ראש צוות' in title or 'ראש צוות' in description:
        return 'Team Leader'
    elif 'tech lead' in title or 'tech lead' in description:
        return 'Tech Lead'
    elif 'embedded' in title or 'embedded' in description:
        return 'Embedded'
    elif 'c++' in title or 'c++' in description:
        return 'C++'
    elif 'java' in title or 'java' in description:
        return 'Backend'
    elif 'net' in title or 'net' in description:
        return 'Backend'
    elif 'ארכיטקט/ית' in title or 'ארכיטקט/ית' in description:
        return 'Architect'
    elif 'crm' in title or 'crm' in description:
        return 'CRM Developer'
    elif 'sap' in title or 'sap' in description:
        return 'SAP Developer'
    elif 'gis' in title or 'gis' in description:
        return 'GIS Developer'
    elif 'cobol' in title or 'cobol' in description:
        return 'COBOL'
    elif 'siebel' in title or 'siebel' in description:
        return 'Siebel Developer'
    elif 'scrum' in title or 'scrum' in description:
        return 'Scrum Master'
    else:
        return 'Other'

def extract_requirements(requirements_text):
    requirements = []

    skills_list = [
        'Frontend', 'Backend', 'Fullstack', 'Software Developer', 'Software Engineer', 'Team Leader', 'Tech Lead',
        'צד לקוח', 'צד שרת', 'מפתח/ת תוכנה', 'מהנדס/ת תוכנה',
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C#', 'C\\+\\+', 'SQL', 'Ruby', 'PHP',
        'React', 'Angular', 'Vue', '.NET', 'Spring Boot', 'Django', 'Flask', 'Node\\.js', 
        'Microservices', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Agile', 'Spring', 'Cobol', 'Embedded', 'ABAP', 'Siebel', 'scrum'
    ]

    skills_pattern = '|'.join(skills_list)
    experience_pattern = re.compile(r'(\d+|שנה|שנתיים|years?|שנים|one|two|three|four|five)', re.IGNORECASE)

    experience_words_to_numbers = {
        'שנה': 1,
        'שנתיים': 2,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'year': 1,
        'years': 1
    }

    lines = re.split(r'\n', requirements_text)
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        skill_match = re.findall(skills_pattern, line, re.IGNORECASE)
        experience_match = experience_pattern.search(line)

        if experience_match:
            experience_text = experience_match.group(1).lower()
            experience_years = experience_words_to_numbers.get(experience_text, None)
            
            if experience_years is None:
                experience_years = int(experience_text)
        else:
            experience_years = 0

        if skill_match:
            for skill in skill_match:
                skill = skill.strip()
                requirements.append({'skill': skill, 'experience': experience_years})

    return requirements

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
            'source': platform_name,
            'scraped_at': datetime.now(),
        }
    except Exception as e:
        logger.error(f'Error processing job listing: {e}')
        return None
