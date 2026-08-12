import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
from config import WEIGHT_SKILL, WEIGHT_TFIDF

def load_job_roles(csv_path: str) -> List[Dict]:
    """
    Loads and validates the job roles from a CSV file.
    Each row contains role_name, description, semicolon-separated required_skills,
    semicolon-separated preferred_skills, and semicolon-separated learning_topics.
    """
    try:
        df = pd.read_csv(csv_path)
        roles = []
        for _, row in df.iterrows():
            req = [s.strip() for s in str(row["required_skills"]).split(";") if s.strip()]
            pref = [s.strip() for s in str(row.get("preferred_skills", "")).split(";") if s.strip()]
            topics = [t.strip() for t in str(row.get("learning_topics", "")).split(";") if t.strip()]
            
            roles.append({
                "role_name": str(row["role_name"]).strip(),
                "description": str(row["description"]).strip(),
                "required_skills": req,
                "preferred_skills": pref,
                "learning_topics": topics
            })
        return roles
    except Exception as e:
        raise ValueError(f"Error loading job roles: {str(e)}")

def build_role_text_representation(role: Dict) -> str:
    """Creates a text block representing the job role for TF-IDF vectorization."""
    # We combine role name, description, required skills, and preferred skills
    parts = [
        role["role_name"],
        role["description"],
        " ".join(role["required_skills"]),
        " ".join(role["preferred_skills"]),
        " ".join(role["learning_topics"])
    ]
    return " ".join(parts).lower()

def match_resume_to_roles(
    cleaned_resume_text: str,
    detected_skills: List[str],
    job_roles: List[Dict]
) -> List[Dict]:
    """
    Compares resume against all job roles and calculates:
      - Skill Score (70% weight)
      - TF-IDF Cosine Similarity (30% weight)
      - Combined Score
    Returns a sorted list of roles with matching details.
    """
    if not job_roles:
        return []
    
    # 1. Calculate TF-IDF similarities
    role_texts = [build_role_text_representation(r) for r in job_roles]
    
    # Custom token pattern to preserve C++, C#, .NET, scikit-learn, etc.
    vectorizer = TfidfVectorizer(token_pattern=r"[a-z0-9\+\#\.\-\/]+")
    
    # Combine resume and role texts for fitting
    corpus = [cleaned_resume_text] + role_texts
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    resume_vec = tfidf_matrix[0]
    role_vecs = tfidf_matrix[1:]
    
    # Cosine similarity matches
    similarities = cosine_similarity(resume_vec, role_vecs)[0]
    
    # 2. Calculate Skill Overlap and Combined Score
    results = []
    resume_skills_set = set(s.lower() for s in detected_skills)
    
    for i, role in enumerate(job_roles):
        # Case-insensitive overlap for required skills
        req_skills = role["required_skills"]
        req_matched = [s for s in req_skills if s.lower() in resume_skills_set]
        req_missing = [s for s in req_skills if s.lower() not in resume_skills_set]
        
        # Case-insensitive overlap for preferred skills
        pref_skills = role["preferred_skills"]
        pref_matched = [s for s in pref_skills if s.lower() in resume_skills_set]
        pref_missing = [s for s in pref_skills if s.lower() not in resume_skills_set]
        
        # Skill Score calculation
        if req_skills:
            skill_score = (len(req_matched) / len(req_skills)) * 100.0
        else:
            skill_score = 0.0
            
        tfidf_score = float(similarities[i]) * 100.0
        
        # Combined score calculation
        combined_score = (WEIGHT_SKILL * skill_score) + (WEIGHT_TFIDF * tfidf_score)
        
        results.append({
            "role_name": role["role_name"],
            "description": role["description"],
            "skill_score": round(skill_score, 1),
            "tfidf_score": round(tfidf_score, 1),
            "combined_score": round(combined_score, 1),
            "matched_required_skills": req_matched,
            "missing_required_skills": req_missing,
            "matched_preferred_skills": pref_matched,
            "missing_preferred_skills": pref_missing,
            "learning_topics": role["learning_topics"]
        })
        
    # Sort roles by combined score in descending order
    results = sorted(results, key=lambda x: x["combined_score"], reverse=True)
    return results
