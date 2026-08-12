import re
import pandas as pd
from typing import Dict, List, Set, Tuple

def load_skill_dictionary(csv_path: str) -> List[Dict]:
    """
    Loads and parses the skill dictionary from a CSV file.
    Each row contains skill_name, category, and semicolon-separated aliases.
    """
    try:
        df = pd.read_csv(csv_path)
        skills = []
        for _, row in df.iterrows():
            name = str(row["skill_name"]).strip()
            category = str(row["category"]).strip()
            aliases_raw = str(row.get("aliases", ""))
            
            # Semicolon separated aliases
            aliases = [a.strip().lower() for a in aliases_raw.split(";") if a.strip()]
            
            # Ensure the lowercase canonical name is also an alias
            if name.lower() not in aliases:
                aliases.append(name.lower())
                
            skills.append({
                "name": name,
                "category": category,
                "aliases": aliases
            })
        return skills
    except Exception as e:
        raise ValueError(f"Error loading skill dictionary: {str(e)}")

def extract_skills(cleaned_text: str, skill_dict: List[Dict]) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    Extracts skills from cleaned text using controlled aliases and regex boundary assertions.
    Returns:
      - Categorized dict: {category: [skills]}
      - Flat list: [skills]
    """
    detected_skills = []
    categorized_skills = {}
    
    # We will search the cleaned text
    # Cleaned text is already lowercase, but we do a safe check
    text_to_search = cleaned_text.lower()
    
    for skill in skill_dict:
        name = skill["name"]
        category = skill["category"]
        aliases = skill["aliases"]
        
        matched = False
        for alias in aliases:
            # Escape regex characters
            escaped_alias = re.escape(alias)
            
            # Lookbehind and lookahead using negative assertions for letters, numbers,
            # and key special characters (+, #, ., -, /) to prevent substring matching
            pattern = rf'(?<![a-z0-9\+#\.\-\/]){escaped_alias}(?![a-z0-9\+#\.\-\/])'
            
            if re.search(pattern, text_to_search):
                matched = True
                break
                
        if matched:
            detected_skills.append(name)
            if category not in categorized_skills:
                categorized_skills[category] = []
            categorized_skills[category].append(name)
            
    # Sort results alphabetically
    detected_skills = sorted(list(set(detected_skills)))
    for cat in categorized_skills:
        categorized_skills[cat] = sorted(list(set(categorized_skills[cat])))
        
    return categorized_skills, detected_skills
