import re

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
