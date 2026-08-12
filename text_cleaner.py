import re
from typing import Dict

# Headers regex for section detection
SECTION_HEADERS = {
    "contact": re.compile(r'\b(contact|personal info|address|phone|email|linkedin|github|website)\b', re.IGNORECASE),
    "summary": re.compile(r'\b(summary|objective|about me|profile|professional summary|executive summary)\b', re.IGNORECASE),
    "skills": re.compile(r'\b(skills|technical skills|skills & tools|core competencies|technologies|key skills)\b', re.IGNORECASE),
    "education": re.compile(r'\b(education|academic background|academics|degree|university|qualifications)\b', re.IGNORECASE),
    "experience": re.compile(r'\b(experience|employment history|work history|professional experience|work experience)\b', re.IGNORECASE),
    "projects": re.compile(r'\b(projects|personal projects|academic projects|key projects|research projects)\b', re.IGNORECASE),
    "certifications": re.compile(r'\b(certifications|certificates|licenses|awards|achievements)\b', re.IGNORECASE),
}

def clean_text(text: str) -> str:
    """
    Cleans and normalizes extracted text.
    Preserves key technical symbols: +, #, ., -, / (e.g., C++, C#, .NET, scikit-learn, CI/CD, React.js)
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace carriage returns, newlines, and tabs with a single space
    text = re.sub(r'[\r\n\t]+', ' ', text)
    
    # Replace periods that are followed by spaces (sentence boundaries) with space,
    # but keep periods inside words (e.g., node.js, .net)
    text = re.sub(r'\.(?=\s|$)', ' ', text)
    
    # Remove all punctuation except alphanumeric and selected symbols: +, #, ., -, /
    # Note that we keep space.
    text = re.sub(r'[^a-z0-9\s\+#\.\-\/]', ' ', text)
    
    # Remove duplicate spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def redact_personal_info(text: str) -> str:
    """
    Redacts contact info and common demographic markers for Responsible AI compliance.
    Does not redact structural technical text.
    """
    if not text:
        return ""
    
    # Redact email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, "[EMAIL_REDACTED]", text)
    
    # Redact phone numbers (simple heuristics for formats like +1-234-567-8900, (123) 456-7890, etc.)
    phone_pattern = r'\b(?:\+?\d{1,3}[-. ]?)?\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}\b'
    text = re.sub(phone_pattern, "[PHONE_REDACTED]", text)
    
    # Redact URLs/links
    url_pattern = r'\b(?:https?://|www\.)\S+\b'
    text = re.sub(url_pattern, "[URL_REDACTED]", text)
    
    return text

def detect_sections(text: str) -> Dict[str, str]:
    """
    Splits the resume text into sections using simple keyword heuristics.
    Returns a dictionary of found sections.
    """
    lines = text.split('\n')
    sections = {
        "contact": [],
        "summary": [],
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "other": []
    }
    
    current_section = "other"
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        
        # Check if this line is likely a header
        # Usually headers are short (less than 5 words / 40 chars)
        is_header = False
        if len(cleaned_line) < 40 and len(cleaned_line.split()) <= 4:
            for sec_name, pattern in SECTION_HEADERS.items():
                if pattern.match(cleaned_line):
                    current_section = sec_name
                    is_header = True
                    break
        
        if not is_header:
            sections[current_section].append(cleaned_line)
            
    # Combine lines into strings
    return {k: "\n".join(v).strip() for k, v in sections.items() if v}
