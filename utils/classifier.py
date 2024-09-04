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
