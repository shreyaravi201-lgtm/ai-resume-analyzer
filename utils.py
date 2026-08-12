import os
import pandas as pd
from typing import Tuple

def validate_job_roles_csv(file_path: str) -> Tuple[bool, str]:
    """Validates the schema and completeness of job_roles.csv."""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    required_cols = {"role_name", "description", "required_skills", "preferred_skills", "learning_topics"}
    try:
        df = pd.read_csv(file_path)
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            return False, f"Missing required columns in job_roles.csv: {missing_cols}"
        
        # Check for empty cells in critical columns
        if df["role_name"].isnull().any():
            return False, "Found null values in 'role_name' column."
        if df["required_skills"].isnull().any():
            return False, "Found null values in 'required_skills' column."
        
        return True, "Valid"
    except Exception as e:
        return False, f"Error reading job_roles.csv: {str(e)}"

def validate_skill_dictionary_csv(file_path: str) -> Tuple[bool, str]:
    """Validates the schema and completeness of skill_dictionary.csv."""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    required_cols = {"skill_name", "category", "aliases"}
    try:
        df = pd.read_csv(file_path)
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            return False, f"Missing required columns in skill_dictionary.csv: {missing_cols}"
        
        if df["skill_name"].isnull().any():
            return False, "Found null values in 'skill_name' column."
        if df["category"].isnull().any():
            return False, "Found null values in 'category' column."
            
        return True, "Valid"
    except Exception as e:
        return False, f"Error reading skill_dictionary.csv: {str(e)}"
