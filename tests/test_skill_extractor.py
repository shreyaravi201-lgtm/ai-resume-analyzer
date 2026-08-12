import os
import pytest
from skill_extractor import load_skill_dictionary, extract_skills
from config import SKILL_DICTIONARY_PATH

def test_load_skill_dictionary():
    assert os.path.exists(SKILL_DICTIONARY_PATH), "Skill dictionary CSV does not exist."
    skill_dict = load_skill_dictionary(SKILL_DICTIONARY_PATH)
    assert len(skill_dict) >= 30
    assert any(s["name"] == "Python" for s in skill_dict)
    assert any(s["name"] == "Scikit-learn" for s in skill_dict)

def test_extract_skills_simple():
    skill_dict = [
        {"name": "Python", "category": "Programming", "aliases": ["python"]},
        {"name": "Scikit-learn", "category": "Machine Learning", "aliases": ["scikit-learn", "sklearn", "scikit learn"]},
        {"name": "C++", "category": "Programming", "aliases": ["c++", "cpp"]}
    ]
    
    text = "i develop in python using sklearn and some c++ features."
    categorized, flat = extract_skills(text, skill_dict)
    
    assert "Python" in flat
    assert "Scikit-learn" in flat
    assert "C++" in flat
    assert categorized["Programming"] == ["C++", "Python"]
    assert categorized["Machine Learning"] == ["Scikit-learn"]

def test_extract_skills_no_false_positives():
    # Make sure "C" skill alias doesn't match letter c inside other words
    skill_dict = [
        {"name": "C", "category": "Programming", "aliases": ["c"]},
        {"name": "Java", "category": "Programming", "aliases": ["java"]}
    ]
    
    # Text contains 'c' as character, but not as standalone language
    text = "i code in java and learn computer concepts."
    _, flat = extract_skills(text, skill_dict)
    assert "Java" in flat
    assert "C" not in flat, "False positive: matched 'c' inside 'concepts' or 'code'."
    
    # Standalone C language
    text_c = "i code in c and java."
    _, flat_c = extract_skills(text_c, skill_dict)
    assert "C" in flat_c
