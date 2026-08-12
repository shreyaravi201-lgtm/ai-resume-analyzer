import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
SKILL_DICTIONARY_PATH = os.path.join(BASE_DIR, "data", "skill_dictionary.csv")
if not os.path.exists(SKILL_DICTIONARY_PATH):
    SKILL_DICTIONARY_PATH = os.path.join(BASE_DIR, "skill_dictionary.csv")

JOB_ROLES_PATH = os.path.join(BASE_DIR, "data", "job_roles.csv")
if not os.path.exists(JOB_ROLES_PATH):
    JOB_ROLES_PATH = os.path.join(BASE_DIR, "job_roles.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Ensure reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Matching system weights
WEIGHT_SKILL = 0.70
WEIGHT_TFIDF = 0.30

# File upload restrictions
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Match level definitions
MATCH_LEVELS = {
    (0.0, 39.9): "Low Match",
    (40.0, 59.9): "Moderate Match",
    (60.0, 79.9): "Good Match",
    (80.0, 100.001): "Strong Match"
}

def get_match_level(score: float) -> str:
    """Returns the descriptive match level for a given score between 0 and 100."""
    for (low, high), label in MATCH_LEVELS.items():
        if low <= score < high:
            return label
    return "Unknown Match"

# Responsible AI and privacy disclaimer statements
RESPONSIBLE_AI_NOTICE = (
    "This system is designed for educational career guidance. It must not be used as an "
    "automatic hiring, rejection, or recruitment decision system."
)

SCORE_EXPLANATION = (
    "The Combined Match Score is computed using a weighted formula: "
    "**70% Skill Score** (matching required skills in the target role) and "
    "**30% TF-IDF Similarity Score** (matching semantic vocabulary using Cosine Similarity). "
    "Match scores are estimates and should not be interpreted as definitive recruiter decisions."
)

MISSING_SKILL_WARNING = (
    "A missing keyword does not necessarily mean you lack the actual ability. "
    "It indicates the term was not detected using our controlled skill patterns. "
    "Ensure your resume clearly lists your tools, projects, and experiences."
)

PRIVACY_STATEMENT = (
    "Responsible AI & Privacy: Uploaded resumes are parsed in-memory, processed temporarily, and "
    "never stored on disk or sent to any external APIs. Personal demographics (names, contact info, etc.) "
    "are not stored or used for scoring."
)
