import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def classify_job_position(title, description):
    if 'full stack' in title.lower() or 'full stack' in description.lower():
        return 'Fullstack'
    elif 'backend' in title.lower() or 'backend' in description.lower():
        return 'Backend'
    elif 'frontend' in title.lower() or 'frontend' in description.lower():
        return 'Frontend'
    elif 'מפתח/ת תוכנה' in title or 'מפתח/ת תוכנה' in description:
        return 'Software Developer'
    elif 'ראש צוות' in title or 'ראש צוות' in description:
        return 'Team Leader'
    elif 'Embedded' in title or 'Embedded' in description:
        return 'Embedded'
    elif 'Java' in title or 'Java' in description:
        return 'Java'
    else:
        return 'Other'

def extract_requirements(requirements_text):
    requirements = []

    skills_list = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C#', 'C\\+\\+', 'SQL', 'Ruby', 'PHP',
        'React', 'Angular', 'Vue', '.NET', 'Spring Boot', 'Django', 'Flask', 'Node\\.js', 
        'Microservices', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'Agile', 'Spring'
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

def parse_job_listing(job, platform_name):
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
