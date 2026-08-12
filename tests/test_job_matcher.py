import os
import pytest
from job_matcher import load_job_roles, build_role_text_representation, match_resume_to_roles
from config import JOB_ROLES_PATH

def test_load_job_roles():
    assert os.path.exists(JOB_ROLES_PATH)
    roles = load_job_roles(JOB_ROLES_PATH)
    assert len(roles) >= 10
    assert any(r["role_name"] == "Machine Learning Engineer" for r in roles)

def test_match_resume_to_roles():
    job_roles = [
        {
            "role_name": "Data Analyst",
            "description": "Analyzes data with SQL and Power BI.",
            "required_skills": ["SQL", "Power BI", "Python"],
            "preferred_skills": ["Excel"],
            "learning_topics": ["SQL joins", "Power BI visualizations"]
        },
        {
            "role_name": "Machine Learning Engineer",
            "description": "Builds models with Python and Scikit-learn.",
            "required_skills": ["Python", "Machine Learning", "Scikit-learn"],
            "preferred_skills": ["Docker"],
            "learning_topics": ["Model building", "Deployment"]
        }
    ]
    
    # Resume matches ML role required skills fully
    detected_skills = ["Python", "Machine Learning", "Scikit-learn"]
    cleaned_resume = "python developer building machine learning models with scikit-learn. interested in tensorflow."
    
    results = match_resume_to_roles(cleaned_resume, detected_skills, job_roles)
    
    assert len(results) == 2
    # ML Engineer should rank first since skill match is 100% (3/3), while Data Analyst has only Python (1/3 = 33%)
    assert results[0]["role_name"] == "Machine Learning Engineer"
    assert results[0]["skill_score"] == 100.0
    assert results[0]["combined_score"] > results[1]["combined_score"]
